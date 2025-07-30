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
        self._add_routes()
