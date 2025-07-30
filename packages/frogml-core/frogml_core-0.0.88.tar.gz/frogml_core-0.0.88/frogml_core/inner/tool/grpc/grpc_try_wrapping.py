import logging
from typing import Callable

import grpc

from frogml_core.exceptions import FrogmlException


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def grpc_try_catch_wrapper(exception_message: str):
    def decorator(function: Callable):
        def _inner_wrapper(*args, **kwargs):
            try:
                logger.debug(
                    "About to call gRPC function: %s where *args = %s and **kwargs = %s",
                    function.__name__,
                    args,
                    kwargs,
                )
                return function(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    "An exception occurred in gRPC function %s. Exception: %s",
                    function.__name__,
                    e,
                )
                if isinstance(e, grpc.RpcError):
                    # noinspection PyUnresolvedReferences
                    raise FrogmlException(
                        exception_message + f". Error is: {e.details()}."
                    ) from e

                raise e

        return _inner_wrapper

    return decorator
