from dependency_injector import containers, providers

from frogml_core.model.decorators.impl.api_implementation import (
    create_decorator_function,
)
from frogml_core.model.decorators.impl.timer_implementation import create_frogml_timer


class FrogmlRuntimeContainer(containers.DeclarativeContainer):
    """
    Frogml Core's Runtime Dependency Injection Container
    """

    api_decorator_function_creator = providers.Object(create_decorator_function)
    timer_function_creator = providers.Object(create_frogml_timer)


class ContainerLock:
    locked: bool = False
