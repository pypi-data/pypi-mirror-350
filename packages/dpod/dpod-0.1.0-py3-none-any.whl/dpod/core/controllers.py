import asyncio
import functools
import json
import pathlib
from urllib.parse import urlparse
from typing import Optional

from click import Group
import questionary
import zmq
from zmq.asyncio import Context
import docker
from docker.errors import NotFound, ImageNotFound, APIError

from dpod.core.dtos import PodData


from .deps import USER_PATH_LOCATION
from .interfaces import AuthControllerABC, ConfigControllerABC, ConfigRepoABC, DeploymentControllerABC, ImageStorageRepoABC, LoggerServiceABC, ImageControllerABC


def async_to_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))
        return result
    return wrapper

class ImageController(ImageControllerABC):
    cli: Group
    image_storage_repo: ImageStorageRepoABC
    config_repo: ConfigRepoABC
    logger: LoggerServiceABC
    user_path_loc: USER_PATH_LOCATION

    def reg_commands(self):
        image = self.cli.group()(self.image)
        image.command()(async_to_sync(self.reg))
        image.command()(async_to_sync(self.build_and_upload))

    def image(self):
        ...

    async def reg(self):
        try:
            # Шаг 1: Подтверждение пути
            docker_folder_default = self.user_path_loc
            docker_folder = await questionary.text(
                f"Под этим ли путём мы хотим зарегистрировать pod image?\n{docker_folder_default}"
            ).ask_async()
            if not docker_folder:
                docker_folder = docker_folder_default

            # Шаг 2: Выбор репозитория
            repository = await questionary.text(
                "В какой репозиторий вы будете заливать данный образ ?",
            ).ask_async()

            # Шаг 3: Имя образа
            image_name = await questionary.text(
                "Под каким именем регистрируем репозиторий:"
            ).ask_async()

            self.config_repo.update_config("image_info", 
                json.dumps(
                    dict(
                        docker_folder=docker_folder,
                        image_name=image_name,
                        repository=repository
                        )   
                ))
            
            # # Шаг 4: Отправка в Dispersion Core
            # image_url = await self.image_storage_repo.push_image(
            #     image_name=image_name,
            #     repository=repository)
            self.logger.success(f"Информация об образе сохранена")

        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}")

    async def build_and_upload(self):
        image_info = json.loads(self.config_repo.get_config_value("image_info"))

        docker_folder = image_info['docker_folder']
        image_name = image_info['image_name']
        repository = image_info['repository']

        try:
            await self.image_storage_repo.delete_latest_tag()
        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}")
        status, message = self.image_storage_repo.build_image(docker_folder, image_name)
        if not status:
            self.logger.error(f"Ошибка: {message}")
            raise
        push_status = self.image_storage_repo.push_image(image_info['image_name'], image_info['repository'])


class AuthController(AuthControllerABC):
    cli: Group
    image_storage_repo: ImageStorageRepoABC
    config_repo: ConfigRepoABC

    def reg_commands(self):
        auth_group = self.cli.group()(self.auth)
        auth_group.command()(async_to_sync(self.set_storage_url))
        auth_group.command()(async_to_sync(self.login))

    def auth(self):
        ...

    async def set_storage_url(self):
        image_storage_url: str = await questionary.text(
                "укажите url хранилища:"
            ).ask_async()
        self.config_repo.update_config("image_storage_url", image_storage_url)

    async def login(self):
        # TODO: перенести в config controller
        login: str = await questionary.text("укажите логин:").ask_async()
        password: str = await questionary.password("укажите пароль:").ask_async()
        registry_url: Optional[str] = self.config_repo.get_config_value("image_storage_url")

        self.config_repo.update_config("username", login)
        self.config_repo.update_config("password", password)

        if not registry_url:
            self.logger.error("не указан url хранилища")
            return


class ConfigController(ConfigControllerABC):
    cli: Group
    config_repo: ConfigRepoABC

    def reg_commands(self):
        config = self.cli.group()(self.config)
        config.command()(self.config_repo.init_config)
        config.command()(self.set_dispersion_core_url)

    def config(self):
        ...

    def set_dispersion_core_url(self):
        value: str = questionary.text("укажите url Dispersion Core:").ask()
        self.config_repo.update_config("disperion_core_url", value)

        try:
            parsed_url = urlparse(value)
            if not parsed_url.hostname:
                raise ValueError
            self.config_repo.update_config("disperion_core_hostname", parsed_url.hostname)
        except ValueError:
            self.logger.error("не могу извлечь hostname из url")


class DeploymentController(DeploymentControllerABC):
    cli: Group
    config_repo: ConfigRepoABC

    def reg_commands(self):
        config = self.cli.group()(self.deploy)
        config.command(async_to_sync(self.listen_for_events))
    
    def deploy(self):
        ...

    def setup_connection(self):
        self.context = Context()

        hostname = self.config_repo.get_config_value("disperion_core_hostname")

        # Сокеты
        self.task_receiver = self.context.socket(zmq.PULL)
        self.confirmation_sender = self.context.socket(zmq.PUSH)
        self.status_subscriber = self.context.socket(zmq.SUB)

        self.task_receiver.connect(f"tcp://{hostname}:5555")
        self.confirmation_sender.connect(f"tcp://{hostname}:5556")
        self.status_subscriber.connect(f"tcp://{hostname}:5557")
        # self.status_subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    async def listen_for_events(self):
        self.setup_connection()
        while True:
            event = await self.task_receiver.recv_json()
            await self.handle_event(event)
            print(f"recieved event: {event}")
            # print(f"[{self.client_id}] Начата задача {task_id}: {data}")

    # TODO: должно быть в сервисе
    async def handle_event(self, event):
        # await self.status_subscriber.send_json(event)
        task_id, data = event["task_id"], event["data"]

        if event['type'] == "deploy":
            await self.deploy_container(data['pod'])

        await self.confirmation_sender.send_json({"task_id": task_id})
        print(f"Задача {task_id} завершена")


    async def deploy_container(self, data: PodData):
        client = docker.from_env()
        harbor_domain = self.config_repo.get_config_value("image_storage_url")
        harbor_domain = urlparse(harbor_domain).hostname
        new_image_name = f"{harbor_domain}/{data['pod_name']}"

        docker_settings = [el for el in data['settings'] if 'name' in el and el['name'] == "docker_settings"][0]['values']

        try:
            # Пытаемся получить существующий контейнер
            container = client.containers.get(data['name'])
            needs_update = False
            old_image = container.image

            # Проверяем изменения параметров
            if data["pod_name"] != container.image.tags[0]:
                needs_update = True

            # TODO: добавить сравнение тегов
            # if data[""]

            # Проверяем изменения переменных окружения
            if 'envs' in docker_settings:
                current_env = {k: v for k, v in [e.split('=', 1) for e in container.attrs['Config']['Env']]}
                new_env = docker_settings.get('envs', {})
                if current_env != new_env:
                    needs_update = True

            if needs_update:
                print(f"Обнаружены изменения для контейнера '{data["name"]}', начинаю обновление...")

                # Скачиваем новый образ
                # TODO: установка должна учитывать тэг
                client.images.pull(new_image_name)

                # Останавливаем и удаляем старый контейнер
                container.stop()
                container.remove()

                # Удаляем старый образ (если не используется другими контейнерами)
                try:
                    client.images.remove(old_image.tags[0])
                except Exception as e:
                    print(f"Не удалось удалить образ: {e}")

                # Создаём новый контейнер
                new_container = client.containers.create(
                    image=new_image_name,
                    name=data["name"],
                    **docker_settings
                )
                new_container.start()
                print(f"Контейнер '{data["name"]}' успешно обновлён")

            else:
                print(f"Контейнер '{data["name"]}' не требует обновления")

        except NotFound:
            # Если контейнер не существует - создаём новый
            print(f"Создание нового контейнера '{data["name"]}'. Используется образ {new_image_name}")
            client.images.pull(new_image_name)
            new_container = client.containers.create(
                image=new_image_name,
                name=data['name'],
                **docker_settings
            )
            new_container.start()
            print(f"Контейнер '{data["name"]}' успешно создан")

    async def create_network(self):
        """Создаёт новую сеть Docker, если она не существует."""
        client = docker.from_env()
        try:
            # Проверяем существование сети
            client.networks.get(network_name)
            print(f"Сеть '{network_name}' уже существует")
        except NotFound:
            # Создаём сеть, если её нет
            client.networks.create(network_name, driver="bridge")
            print(f"Сеть '{network_name}' успешно создана")
        except APIError as e:
            print(f"Ошибка при работе с сетью: {e}")

