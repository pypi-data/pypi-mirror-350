from abc import ABC, abstractmethod

from archtool.components.default_component import ComponentPattern
from archtool.global_types import AppModules
from archtool.layers import Layer

from archtool.layers.default_layer_interfaces import (ABCView,
                                                      ABCService,
                                                      ABCRepo,
                                                      ABCController)
from archtool.layers.default_layers import (ApplicationLayer,
                                            DomainLayer,
                                            InfrastructureLayer)


from typing import Any, Callable, Dict, Optional, Sequence, Set, Type, Union, Unpack
from enum import Enum
from typing_extensions import TypedDict


class PresentationLayer(Layer):
    """
    Слой отображения
    """
    depends_on = ApplicationLayer or DomainLayer

    class Components:
        views = ComponentPattern(module_name_regex="views",
                                 superclass=ABCView)
        # endpoints_initializers = ComponentPattern(
        #                          module_name_regex="views",
        #                          superclass=RoutersInitializationStrategyABC)

# TODO: нужно добавить режим импорта, без использования интерфейсов.
# Эти объекты не должны находиться в зависимостях, нужно просто импортировать файлы
# Либо зависимости необходимо украдывать в список и вешать на него ключ зависимостями
#  
# class InfrastructureLayer(Layer):
#     class Components:
#         models = ComponentPattern(module_name_regex="models",
#                                   superclass=DeclarativeBase)


app_layers = frozenset([PresentationLayer,
                        ApplicationLayer,
                        DomainLayer,
                        InfrastructureLayer])


from archtool.global_types import AppModule


APPS: AppModules = [
    AppModule('dpod.core'),
]
