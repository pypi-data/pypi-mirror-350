from abc import abstractmethod
from typing import Any, Optional
from archtool.layers.default_layer_interfaces import ABCController, ABCService, ABCRepo
from web_fractal.cli.interfaces import CommanderControllerABC


class ImageControllerABC(CommanderControllerABC, ABCController):
    @abstractmethod
    async def reg(self):
        """
        добавляет image в harbor репозиторий, запускает сборку контейнера,
        пушит его
        """
        ...

class AuthControllerABC(CommanderControllerABC, ABCController):
    @abstractmethod
    async def login(self):
        ...


class ImageStorageRepoABC(ABCRepo):
    """
    интерфейс репозитория, который импленентирует логику взаимодействия с
    физическим хранилищем образов docker (например harbor)
    """
    @abstractmethod
    async def push_image(self, image_name: str, repository: str) -> str:
        """
        публикует образ в хранилище
        """
        ...

    @abstractmethod
    def build_image(dockerfile_dir: str, tag: str) -> tuple[bool, Optional[str]]:
        ...
    
    @abstractmethod
    def docker_login(self) -> bool:
        ...

    @abstractmethod
    def push_image(self, image_tag: str, project: str) -> bool:
        ...
    
    @abstractmethod
    async def delete_latest_tag(self) -> bool:
        ...


class ConfigRepoABC(ABCRepo):
    
    @abstractmethod
    def init_config(self):
        """
        инициализирует пустой конфиг в папке, из которой вызывается команда
        """
        ...

    @abstractmethod
    def get_config_content(self) -> dict[str, Any]:
        """
        достаёт всё содержимое конфига
        """
        ...

    @abstractmethod
    def update_config(self, key, new_value) -> None:
        """
        обновляет значенние конфига
        """
        ...

    @abstractmethod
    def get_config_value(self, key: str) -> Any:
        """
        достаёт значение конфига по ключу
        """
        ...


class LoggerServiceABC(ABCService):
    @abstractmethod
    def error(self, message: str):
        ...

    @abstractmethod
    def success(self, message: str):
        ...

    @abstractmethod
    def info(self, message: str):
        ...


class ConfigControllerABC(CommanderControllerABC, ABCController):
    @abstractmethod
    def config(self):
        ...


class DeploymentControllerABC(CommanderControllerABC, ABCController):
    @abstractmethod
    async def listen_for_events(self):
        ...

    @abstractmethod
    async def handle_event(self, event: dict):
        ...
    