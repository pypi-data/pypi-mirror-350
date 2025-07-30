import uuid
from datetime import datetime
from typing import Dict

from google.protobuf.timestamp_pb2 import Timestamp

from frogml_proto.jfml.model_version.v1.model_repository_spec_pb2 import (
    ModelRepositorySpec,
)
from frogml_proto.jfml.model_version.v1.model_version_framework_pb2 import (
    CatboostFramework,
)
from frogml_proto.jfml.model_version.v1.model_version_manager_service_pb2 import (
    CreateModelVersionResponse,
    CreateModelVersionRequest,
    GetModelVersionByIdResponse,
    GetModelVersionByIdRequest,
    GetModelVersionByNameRequest,
    GetModelVersionByNameResponse,
    InitPaginationRequest,
    InitPaginationResponse,
    ListModelVersionsRequest,
    ListModelVersionsResponse,
    DeleteModelVersionByIdRequest,
    DeleteModelVersionByIdResponse,
    PromoteModelVersionToBuildRequest,
    PromoteModelVersionToBuildResponse,
    GetMlBomModelVersionByIdRequest,
    GetMlBomModelVersionByIdResponse,
)
from frogml_proto.jfml.model_version.v1.model_version_manager_service_pb2_grpc import (
    ModelVersionManagerServiceServicer,
)
from frogml_proto.jfml.model_version.v1.model_version_pb2 import (
    ModelVersion,
    ModelVersionCompletedStatus,
    ModelVersionSpec,
    ModelVersionStatus,
)

timestamp = Timestamp()
timestamp.FromDatetime(datetime.now())


class ModelVersionManagerServiceMock(ModelVersionManagerServiceServicer):
    def __init__(self):
        super(ModelVersionManagerServiceMock, self).__init__()
        self.model_versions: Dict[str, ModelVersion] = {}

    def CreateModelVersion(
        self, request: CreateModelVersionRequest, context
    ) -> CreateModelVersionResponse:
        return CreateModelVersionResponse(
            model_version=ModelVersion(
                model_version_id=str(uuid.uuid4()),
                spec=request.model_version,
                status=ModelVersionStatus(completed=ModelVersionCompletedStatus()),
                created_by="mock",
                created_at=timestamp,
                updated_at=timestamp,
            )
        )

    def GetModelVersionById(
        self, request: GetModelVersionByIdRequest, context
    ) -> GetModelVersionByIdResponse:
        return GetModelVersionByIdResponse(
            model_version=ModelVersion(
                model_version_id=request.model_version_id,
                spec=ModelVersionSpec(
                    repository_spec=ModelRepositorySpec(
                        project_key="mock-project",
                        repository_key="mock-repository",
                        model_id=str(uuid.uuid4()),
                    ),
                    name="mock-model-version-name",
                    framework=CatboostFramework(),
                    python_version="3.9",
                ),
                status=ModelVersionStatus(completed=ModelVersionCompletedStatus()),
                created_by="mock",
                created_at=timestamp,
                updated_at=timestamp,
            )
        )

    def GetModelVersionByName(self, request: GetModelVersionByNameRequest, context):
        return GetModelVersionByNameResponse(
            model_version=ModelVersion(
                model_version_id=str(uuid.uuid4()),
                spec=ModelVersionSpec(
                    repository_spec=ModelRepositorySpec(
                        project_key="mock-project",
                        repository_key="mock-repository",
                        model_id=request.model_id,
                    ),
                    name=request.model_version_name,
                    framework=CatboostFramework(),
                    python_version="3.9",
                ),
                status=ModelVersionCompletedStatus(),
                created_by="mock",
                created_at=timestamp,
                updated_at=timestamp,
            )
        )

    def InitPagination(
        self, request: InitPaginationRequest, context
    ) -> InitPaginationResponse:
        return super().InitPagination(request, context)

    def ListModelVersions(
        self, request: ListModelVersionsRequest, context
    ) -> ListModelVersionsResponse:
        return super().ListModelVersions(request, context)

    def DeleteModelVersionById(
        self, request: DeleteModelVersionByIdRequest, context
    ) -> DeleteModelVersionByIdResponse:
        return super().DeleteModelVersionById(request, context)

    def PromoteModelVersionToBuild(
        self, request: PromoteModelVersionToBuildRequest, context
    ) -> PromoteModelVersionToBuildResponse:
        return super().PromoteModelVersionToBuild(request, context)

    def GetMlBomModelVersionById(
        self, request: GetMlBomModelVersionByIdRequest, context
    ) -> GetMlBomModelVersionByIdResponse:
        return super().GetMlBomModelVersionById(request, context)
