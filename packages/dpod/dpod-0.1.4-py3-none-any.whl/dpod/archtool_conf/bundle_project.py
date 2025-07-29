import asyncio
import pathlib

import click
from archtool.dependency_injector import DependencyInjector
from archtool.global_types import AppModule

from web_fractal.building_utils import import_all_models, initialize_controllers_api
from web_fractal.db import Base
from web_fractal.db import init_db

import dpod.config as settings
from dpod.core.deps import USER_PATH_LOCATION
from .custom_layers import APPS, app_layers



@click.group()
@click.version_option("1.0.0")
def cli():
    """Dispersion Platform CLI"""
    ...


def init_deps(injector: DependencyInjector, initial_folder: pathlib.Path):
    injector._reg_dependency(click.Group, cli)
    injector._reg_dependency(USER_PATH_LOCATION, initial_folder)



def bundle(initial_folder) -> DependencyInjector:
    import sys
    apps_root = pathlib.Path.cwd()
    sys.path.insert(0, apps_root.as_posix())
    injector = DependencyInjector(modules_list=APPS, layers=app_layers)
    init_deps(injector=injector, initial_folder=initial_folder)
    injector.inject()
    initialize_controllers_api(injector=injector)
    return injector
