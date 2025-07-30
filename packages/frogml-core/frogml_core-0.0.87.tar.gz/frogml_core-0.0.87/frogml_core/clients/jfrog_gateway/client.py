from typing import cast

from dependency_injector.wiring import Provide, inject

from frogml_core.exceptions import FrogmlException
from frogml_core.inner.di_configuration import FrogmlContainer
from frogml_proto.qwak.jfrog.gateway.v0.repository_service_pb2 import (
    GetRepositoryConfigurationResponse,
    GetRepositoryConfigurationRequest,
)
from frogml_proto.qwak.jfrog.gateway.v0.repository_service_pb2_grpc import (
    RepositoryServiceStub,
)


class JfrogGatewayClient:
    """
    Used for interacting with Feature Registry endpoints
    """

    @inject
    def __init__(self, grpc_channel=Provide[FrogmlContainer.core_grpc_channel]):
        self.__repository_service = RepositoryServiceStub(grpc_channel)

    def get_repository_configuration(
        self, repository_key: str
    ) -> GetRepositoryConfigurationResponse:
        """
        Get repository configuration
        :param repository_key: Repository name
        :return: Model
        """
        request = GetRepositoryConfigurationRequest(repository_key=repository_key)

        try:
            return cast(
                GetRepositoryConfigurationResponse,
                self.__repository_service.GetRepositoryConfiguration(request),
            )
        except Exception as e:
            raise FrogmlException(f"Failed to get repository configuration: {e}") from e
