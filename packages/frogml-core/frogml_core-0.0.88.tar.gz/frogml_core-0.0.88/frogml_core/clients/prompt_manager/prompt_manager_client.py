import grpc
from dependency_injector.wiring import Provide, inject

from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    CreatePromptRequest as ProtoCreatePromptRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    CreatePromptResponse as ProtoCreatePromptResponse,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    CreatePromptVersionRequest as ProtoCreatePromptVersionRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    CreatePromptVersionResponse as ProtoCreatePromptVersionResponse,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    DeletePromptRequest as ProtoDeletePromptRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    DeletePromptVersionRequest as ProtoDeletePromptVersionRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    GetPromptByNameRequest as ProtoGetPromptByNameRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    GetPromptByNameResponse as ProtoGetPromptByNameResponse,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    GetPromptVersionByPromptNameRequest as ProtoGetPromptVersionByPromptNameRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    GetPromptVersionByPromptNameResponse as ProtoGetPromptVersionByPromptNameResponse,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2 import (
    SetDefaultPromptVersionRequest as ProtoSetDefaultPromptVersionRequest,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_manager_service_pb2_grpc import (
    PromptManagerServiceStub,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_pb2 import Prompt as ProtoPrompt
from frogml_proto.qwak.prompt.v1.prompt.prompt_pb2 import PromptSpec as ProtoPromptSpec
from frogml_proto.qwak.prompt.v1.prompt.prompt_pb2 import (
    PromptVersion as ProtoPromptVersion,
)
from frogml_proto.qwak.prompt.v1.prompt.prompt_pb2 import (
    PromptVersionSpec as ProtoPromptVersionSpec,
)
from frogml_core.exceptions import FrogmlException
from frogml_core.inner.di_configuration import FrogmlContainer


class PromptManagerClient:
    @inject
    def __init__(self, grpc_channel=Provide[FrogmlContainer.core_grpc_channel]):
        self._grpc_client: PromptManagerServiceStub = PromptManagerServiceStub(
            grpc_channel
        )

    def create_prompt(
        self,
        name: str,
        prompt_description: str,
        version_spec: ProtoPromptVersionSpec,
    ) -> ProtoPrompt:
        request = ProtoCreatePromptRequest(
            prompt_name=name,
            prompt_spec=ProtoPromptSpec(description=prompt_description),
            prompt_version_spec=version_spec,
        )
        try:
            response: ProtoCreatePromptResponse = self._grpc_client.CreatePrompt(
                request
            )
            return response.prompt
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise FrogmlException(f"Prompt with name: {name} already exists")
            elif call.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise FrogmlException(
                    f"Got an illegal prompt specification: {call.details()}"
                )
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")

    def create_prompt_version(
        self,
        name: str,
        version_spec: ProtoPromptVersionSpec,
        set_default: bool,
    ) -> ProtoPromptVersion:
        request = ProtoCreatePromptVersionRequest(
            prompt_name=name, prompt_version_spec=version_spec, set_default=set_default
        )
        try:
            response: ProtoCreatePromptVersionResponse = (
                self._grpc_client.CreatePromptVersion(request)
            )
            return response.prompt_version
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.NOT_FOUND:
                raise FrogmlException(
                    f"Can not update prompt: '{name}', prompt was not found"
                )
            elif call.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise FrogmlException(
                    f"Got an illegal prompt specification: {call.details()}"
                )
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")

    def delete_prompt(self, name: str):
        try:
            self._grpc_client.DeletePrompt(ProtoDeletePromptRequest(prompt_name=name))
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.NOT_FOUND:
                raise FrogmlException(f"Prompt named '{name}' was not found")
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")

    def delete_prompt_version(self, name: str, version: int):
        try:
            self._grpc_client.DeletePromptVersion(
                ProtoDeletePromptVersionRequest(
                    prompt_name=name, version_number=version
                )
            )
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.NOT_FOUND:
                raise FrogmlException(str(call.details()))
            elif call.code() == grpc.StatusCode.FAILED_PRECONDITION:
                raise FrogmlException(
                    f"Cannot delete the default version '{version}' of a prompt '{name}',"
                    f" please set another version as the default to delete this version."
                )
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")

    def get_prompt_by_name(self, name: str) -> ProtoPrompt:
        """
        Get prompt's default version
        """
        try:
            response: ProtoGetPromptByNameResponse = self._grpc_client.GetPromptByName(
                ProtoGetPromptByNameRequest(prompt_name=name)
            )
            return response.prompt
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.NOT_FOUND:
                raise FrogmlException(str(call.details()))
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")

    def get_prompt_version_by_name(self, name: str, version: int) -> ProtoPromptVersion:
        """
        Get prompt specific version
        """
        try:
            response: ProtoGetPromptVersionByPromptNameResponse = (
                self._grpc_client.GetPromptVersionByPromptName(
                    ProtoGetPromptVersionByPromptNameRequest(
                        prompt_name=name, version_number=version
                    )
                )
            )
            return response.prompt_version
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.NOT_FOUND:
                raise FrogmlException(str(call.details()))
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")

    def set_default_prompt_version(self, name: str, version: int):
        try:
            self._grpc_client.SetDefaultPromptVersion(
                ProtoSetDefaultPromptVersionRequest(
                    prompt_name=name, version_number=version
                )
            )
        except grpc.RpcError as error:
            call: grpc.Call = error  # noqa
            if call.code() == grpc.StatusCode.NOT_FOUND:
                raise FrogmlException(str(call.details()))
            else:
                raise FrogmlException(f"Internal Error: {call.details()}")
