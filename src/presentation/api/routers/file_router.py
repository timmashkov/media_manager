from fastapi import Depends, File, UploadFile

from application.container import Container
from domain.file.entities.model import FileFilter, FileIncomingData, FileResultData
from infrastructure.common.base_entities.base_router import BaseRouter


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
        super()._add_routes()

        @self.api_router.post("/", response_model=FileResultData)
        async def create_object(
            file_in: FileIncomingData = Depends(FileIncomingData.from_form),
            data: UploadFile | None = File(...),
            use_case=Depends(Container.file_service),
        ):
            return await use_case.create_item(data=file_in, file=data)
