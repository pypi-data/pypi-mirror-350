from typing import Any, NotRequired, Union
from uuid import UUID
from web_fractal.db import BaseTypedDict


class SettingsDTO(BaseTypedDict):
    id: UUID
    name: NotRequired[str]
    values: NotRequired[Union[dict[str, Any],'DockerSettings']]


class PodData(BaseTypedDict):
    id: str
    openapi_spec: NotRequired[str]
    name: NotRequired[str]
    dto_name: NotRequired[str]
    project_id: NotRequired[UUID]
    pod_name: NotRequired[str]
    hosting_status: NotRequired[str]
    specification_url: NotRequired[str]
    specification_updated_at: NotRequired[str]
    settings: NotRequired[list[SettingsDTO]]


class DockerSettings(BaseTypedDict):
    envs: NotRequired[dict[str, Any]]
