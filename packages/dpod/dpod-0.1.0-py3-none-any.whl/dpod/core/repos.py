from abc import abstractmethod
import json
import os
import pathlib
from typing import Any, Optional
from urllib.parse import urlparse
import uuid

import docker
from harborapi import HarborAsyncClient

from .interfaces import ConfigRepoABC, ImageStorageRepoABC
from .deps import USER_PATH_LOCATION


class ConfigRepo(ConfigRepoABC):
    initial_folder: USER_PATH_LOCATION
    @property
    def config_path(self) -> pathlib.Path:
        config_path = pathlib.Path(self.initial_folder) / ".dp_config"
        # config_path = pathlib.Path(self.initial_folder) / ".dp_config"
        return config_path

    def init_config(self):
        if self.config_path.exists():
            raise Exception("config already exists")
        else:
            self.config_path.write_text("{}")

    def get_config_content(self) -> dict[str, Any]:
        """
        достаёт всё содержимое конфига
        """
        content = json.loads(self.config_path.read_text())
        return content

    def update_config(self, key, new_value) -> None:
        """
        обновляет значенние конфига
        """
        path = key.split(".")
        config_obj = self.get_config_content()
        current_element = config_obj
        for path_element in path:
            if key != path[-1]:
                current_element = current_element[path_element]
            else:
                current_element[path_element] = new_value
                self.config_path.write_text(json.dumps(config_obj))
                return
        current_element = new_value
        self.config_path.write_text(json.dumps(config_obj))

    def get_config_value(self, key: str) -> Any:
        """
        достаёт значение конфига по ключу
        """
        path = key.split(".")
        config_obj = self.get_config_content()
        current_element = config_obj
        for path_element in path:
            current_element = current_element[path_element]
        return current_element



class HarborRepo(ImageStorageRepoABC):
    config_repo: ConfigRepoABC

    @property
    def client(self) -> HarborAsyncClient:
        registry_url = self.config_repo.get_config_value("image_storage_url")
        client = HarborAsyncClient(
            url="{self.registry_url}/api/v2.0/",
            username=self.config_repo.get_config_value("username"),
            secret=self.config_repo.get_config_value("password"),
        )
        return client

    def build_image(self, dockerfile_dir: str, tag: str) -> tuple[bool, Optional[str]]:
        """
        Собирает Docker-образ из указанной директории
        :param dockerfile_dir: Путь к директории с Dockerfile
        :param tag: Тег для собранного образа (без регистра)
        :return: Кортеж (успех, информация об ошибке)
        """
        client = docker.from_env()
        try:
            # Проверяем существование директории
            if not os.path.isdir(dockerfile_dir):
                return False, f"Directory {dockerfile_dir} not found"
            # Собираем образ
            build_output = client.images.build(
                path=dockerfile_dir,
                tag=tag,
                rm=True,  # Удаляем промежуточные контейнеры
                forcerm=True  # Удаляем временные образы
            )
            print(f"✅ Image built successfully: {build_output[0].tags}")
            return True, None
        
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def docker_login(self) -> bool:
        """
        Авторизация в Docker Registry (Harbor)
        :param registry_url: URL регистра (например: harbor.example.com)
        :param username: Логин пользователя
        :param password: Пароль
        :return: Успех авторизации
        """
        client = docker.from_env()
        try:
            login_response = client.login(
                username=self.config_repo.get_config_value("username"),
                password=self.config_repo.get_config_value("password"),
                registry=self.config_repo.get_config_value("image_storage_url"),
                reauth=False)

            if login_response.get("Status") == "Login Succeeded":
                print("✅ Successfully logged in to registry")
                return True
            return False
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            return False

    def push_image(self, image_tag: str, project: str) -> bool:
        """
        Отправка образа в Harbor Registry
        """
        registry_url = self.config_repo.get_config_value("image_storage_url")
        username = self.config_repo.get_config_value("username")
        password = self.config_repo.get_config_value("password")
        registry_url = urlparse(registry_url).hostname
        client = docker.from_env()
        
        try:
            # 1. Формируем полный тег с учетом URL Harbor
            full_tag = f"{registry_url}/{project}/{image_tag}"
            
            # 2. Тегируем образ для целевого реестра
            image = client.images.get(image_tag)
            image.tag(full_tag)  # Добавляем тег с полным путем
            
            # 3. Авторизация при push
            auth_config = {
                "username": username,
                "password": password
            }
            
            # 4. Отправляем образ с корректным тегом и авторизацией
            push_output = client.images.push(
                repository=full_tag,  # Используем полный тег
                stream=True,
                decode=True,
                auth_config=auth_config  # Добавляем учетные данные
            )
            
            # 5. Анализируем вывод
            for line in push_output:
                if "errorDetail" in line:
                    error = line.get("errorDetail", {}).get("message")
                    print(f"❌ Push failed: {error}")
                    return False
                if "status" in line:
                    print(f"⚡ Status: {line.get('status')}")
                    
            print(f"✅ Image pushed successfully: {full_tag}")
            return True

        except docker.errors.APIError as e:
            print(f"❌ Docker API error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False

    async def delete_latest_tag(
        self,
    ) -> bool:
        """
        Удаляет тег 'latest' с последнего образа в Harbor
        """
        # Инициализация клиента
        client = self.client
        image_info = self.config_repo.get_config_value("image_info")
        docker_folder = image_info['docker_folder']
        image_name = image_info['image_name']
        repository = image_info['repository']

        try:
            # Получаем все артефакты в репозитории
            artifacts = await client.get_artifacts(
                project_name=image_name,
                repository_name=repository,
            )

            # Ищем артефакт с тегом latest
            latest_tag = None
            for artifact in artifacts:
                tags = await client.get_artifact_tags(
                    project_name=image_name,
                    repository_name=repository,
                    reference=artifact.digest,
                )
                for tag in tags:
                    if tag.name == "latest":
                        latest_tag = tag
                        break
                if latest_tag:
                    break
            
            if not latest_tag:
                print(f"❌ Тег 'latest' не найден в {repository}/{image_name}")
                return False
            
            # Удаляем тег
            await client.delete_tag(
                project_name=image_name,
                repository_name=repository,
                reference=artifact.digest,
                tag_name="latest",
            )
            
            print(f"✅ Тег 'latest' успешно удалён из {repository}/{image_name}")
            return True
            
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {str(e)}")
            return False
        finally:
            await client.close()