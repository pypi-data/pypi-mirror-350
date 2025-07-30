import grpc

from frogml_core.exceptions import FrogmlException


def grpc_try_catch_wrapper(exception_message):
    def decorator(function):
        def _inner_wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except grpc.RpcError as e:
                raise FrogmlException(exception_message + f". Error is: {e.details()}.")

        return _inner_wrapper

    return decorator
