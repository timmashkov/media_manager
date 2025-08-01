import typing
import uuid

from starlette.datastructures import UploadFile

from domain.file.entities.model import FileIncomingData
from domain.file.services.file_service import FileService
from infrastructure.common.base_entities.singleton import Singleton
from infrastructure.common.interfaces.minio_client_interface import FileAdapterInterface
from infrastructure.common.interfaces.repository_interfaces import (
    AbstractReadRepository,
    AbstractWriteRepository,
)
from infrastructure.database.models import File


class FileUseCase(Singleton):
    def __init__(
        self,
        read_repository: AbstractReadRepository,
        write_repository: AbstractWriteRepository,
        minio_client: FileAdapterInterface,
    ) -> None:
        self.minio_client = minio_client
        self.read_repository = read_repository
        self.write_repository = write_repository
        self.file_service: FileService = FileService()

    async def get_item(self, uuid: str | uuid.UUID) -> File | None:
        return await self.read_repository.get_item(uuid=uuid)

    async def get_items(self, filters: typing.Any = None) -> typing.List[File]:
        return await self.read_repository.find(filters=filters)

    async def create_item(
        self, data: FileIncomingData, file: UploadFile
    ) -> File | None:
        minio_data, api_data = self.file_service.build_valid_data(
            income_data=data, file=file
        )
        await self.minio_client.upload_file(
            bucket_name=minio_data.bucket,
            object_name=minio_data.object_name,
            data=file.file,
        )
        return await self.write_repository.create_item(**api_data.model_dump())

    async def update_item(
        self, uuid: str | uuid.UUID, data: FileIncomingData
    ) -> File | None:
        intel = data.model_dump()
        intel["uuid"] = uuid
        return await self.write_repository.update_item(**intel)

    async def delete_item(self, uuid: str | uuid.UUID) -> File | None:
        return await self.write_repository.delete_item(uuid=uuid)
