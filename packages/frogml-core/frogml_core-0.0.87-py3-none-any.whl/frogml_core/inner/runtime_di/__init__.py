from frogml_core.inner.runtime_di.containers import (
    ContainerLock,
    FrogmlRuntimeContainer,
)


def wire_runtime():
    container = FrogmlRuntimeContainer()
    from frogml_core.model import decorators

    container.wire(
        packages=[
            decorators,
        ]
    )
    return container
