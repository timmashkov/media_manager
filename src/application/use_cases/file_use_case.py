import asyncio
import typing
import uuid

from starlette.datastructures import UploadFile
from starlette.responses import StreamingResponse, Response

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

    async def download_item(self, uuid: uuid.UUID, stream: bool, download: bool):
        file = await self.read_repository.get_item(uuid=uuid)
        headers = {}
        if download:
            headers["Content-Disposition"] = f"attachment; filename={file.name}"
        if stream:
            return StreamingResponse(
                content=self.minio_client.download_file_chunk(bucket_name=file.bucket, object_name=file.path),
                media_type=file.mimetype,
                headers=headers,
            )
        return Response(
            content=await self.minio_client.download_file(bucket_name=file.bucket, object_name=file.path),
            media_type=file.mimetype,
            headers=headers,
        )

    async def update_item(
        self, uuid: str | uuid.UUID, data: FileIncomingData, file: UploadFile | None,
    ) -> bool:
        minio_data, api_data = self.file_service.build_valid_data(
            income_data=data, file=file
        )
        intel = api_data.model_dump()
        intel["uuid"] = uuid
        bucket, name, tags = await self.write_repository.update_item(**intel)
        await self.minio_client.delete_object(bucket_name=minio_data.bucket, object_name=minio_data.object_name)
        try:
            if file:
                content = file.file
            else:
                content = await self.minio_client.download_file_raw(bucket_name=minio_data.bucket, object_name=minio_data.object_name)
            await self.minio_client.upload_file(
                bucket_name=minio_data.bucket,
                object_name=minio_data.object_name,
                data=content,
                tags=tags,
            )
            return True
        except Exception:
            return False

    async def delete_item(self, uuid: str | uuid.UUID, object_name: str, bucket_name: str) -> bool:
        try:
            await self.minio_client.delete_object(bucket_name=bucket_name, object_name=object_name)
            await self.write_repository.delete_item(uuid=uuid)
            return True
        except Exception:
            return False
