from uuid import UUID

from fastapi import Depends, File, UploadFile

from application.container import Container
from application.use_cases.file_use_case import FileUseCase
from domain.file.entities.model import FileFilter, FileIncomingData, FileResultData, FileBaseData
from infrastructure.common.base_entities.base_router import BaseRouter
from infrastructure.common.common_models.response_models import StatusResponse


class FileRouter(BaseRouter):
    prefix = "/file"
    tags = ["File"]
    filters = FileFilter
    service_client = Container.file_service
    input_model = FileIncomingData
    output_model = FileResultData

    def __init__(self) -> None:
        super().__init__()

    def _add_routes(self) -> None:

        @self.api_router.post("/", response_model=FileResultData)
        async def create_media(
            file_in: FileIncomingData = Depends(FileIncomingData.from_form),
            data: UploadFile | None = File(...),
            use_case: FileUseCase = Depends(Container.file_service),
        ):
            return await use_case.create_item(data=file_in, file=data)

        @self.api_router.get("/{uuid}")
        async def download_media(
                uuid: UUID,
                stream: bool = True,
                download: bool = False,
                use_case: FileUseCase = Depends(Container.file_service),
        ):
            return await use_case.download_item(uuid=uuid, stream=stream, download=download)

        @self.api_router.patch("/{uuid}", response_model=StatusResponse)
        async def update_media(
                uuid: UUID,
                file_in: FileIncomingData = Depends(FileIncomingData.from_form),
                data: UploadFile = File(...),
                use_case: FileUseCase = Depends(Container.file_service),
        ) -> StatusResponse:
            status = await use_case.update_item(uuid=uuid, data=file_in, file=data)
            return StatusResponse(status=status)

        @self.api_router.delete("/{uuid}", response_model=StatusResponse)
        async def delete_media(
                uuid: UUID,
                data: FileBaseData,
                use_case: FileUseCase = Depends(Container.file_service),
        ) -> StatusResponse:
            status = await use_case.delete_item(uuid=uuid, object_name=data.name, bucket_name=data.bucket)
            return StatusResponse(status=status)
