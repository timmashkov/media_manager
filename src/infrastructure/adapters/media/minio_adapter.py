import logging
import typing

import miniopy_async
import tenacity
from miniopy_async.commonconfig import Tags
from urllib3 import BaseHTTPResponse

from application.config import settings
from infrastructure.common.exceptions.minio_exceptions import (
    ObjectNotFound,
    OutDiskSpace,
)
from infrastructure.common.interfaces.minio_client_interface import (
    FileAdapterInterface,
    FileReaderProtocol,
)


class MinioFileAdapter(FileAdapterInterface):
    def __init__(
        self,
        protocol: str,
        host: str,
        port: str | int,
        access_key: str,
        secret_key: str,
        region: str,
        chunk_size: int = 1024,
        logger: logging.Logger | None = None,
    ) -> None:
        self.chunk_size = chunk_size
        self.logger = logger or logging
        self.client = miniopy_async.Minio(
            endpoint=f"{host}:{port}",
            secure=True if protocol == "https" else False,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
        )

    @tenacity.retry(stop=tenacity.stop_after_attempt(2), reraise=True)
    async def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        data: FileReaderProtocol,
        **kwargs: typing.Any,
    ) -> str:
        self.logger.debug("Download file %s to bucket %s...", object_name, bucket_name)
        length = kwargs.pop("length", -1)
        kwargs["part_size"] = 5 * 1024 * 1024 if length == -1 else 0
        minio_tags = Tags(for_object=True)
        if tags := kwargs.pop("tags", {}):
            minio_tags.update(**tags)
        try:
            response = await self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data,
                length=length,
                tags=minio_tags,
                **kwargs,
            )
        except miniopy_async.S3Error as error:
            if error.code == settings.MINIO.ERRORS.NO_SUCH_BUCKET:
                self.logger.warning("Bucket not found %s...", bucket_name)
                await self.client.make_bucket(bucket_name=bucket_name)
                self.logger.info("Bucket %s successfully created", bucket_name)
            if error.code == settings.MINIO.ERRORS.MINIO_STORAGE_FULL:
                raise OutDiskSpace("No free space available")
            if error.code == settings.MINIO.ERRORS.MINIO_QUOTA_FULL:
                raise OutDiskSpace(f"No free space available at bucket: {bucket_name} ")
            raise error
        self.logger.debug(
            "Download %s to bucket %s successfully finished", object_name, bucket_name
        )
        return response.object_name

    async def download_file_raw(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> BaseHTTPResponse:
        self.logger.debug("Download file %s to bucket %s...", object_name, bucket_name)
        try:
            response = await self.client.get_object(
                bucket_name=bucket_name,
                object_name=object_name,
                **kwargs,
            )
        except miniopy_async.S3Error as error:
            if error.code == settings.MINIO.ERRORS.NO_SUCH_FILE:
                raise ObjectNotFound("No such file found")
            raise error
        self.logger.debug(
            "Download %s to bucket %s successfully finished", object_name, bucket_name
        )
        return response

    async def download_file(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> bytes:
        response = None
        try:
            response = await self.download_file_raw(
                bucket_name=bucket_name, object_name=object_name, **kwargs
            )
            return response.data
        finally:
            if response:
                response.close()
                response.release_conn()

    async def download_file_chunk(
        self,
        bucket_name: str,
        object_name: str,
        **kwargs: typing.Any,
    ) -> typing.AsyncGenerator[bytes, None]:
        response = None
        try:
            response = await self.download_file_raw(
                bucket_name=bucket_name, object_name=object_name, **kwargs
            )
            for chunk in response.stream(self.chunk_size):
                yield chunk
        finally:
            if response:
                response.close()
                response.release_conn()

    async def delete_object(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> None:
        await self.client.remove_object(
            bucket_name=bucket_name, object_name=object_name, **kwargs
        )

    async def get_list_objects(
        self, bucket_name: str, **kwargs: typing.Any
    ) -> typing.Iterator:
        return await self.client.list_objects(bucket_name=bucket_name, **kwargs)

    async def check_file_exist(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> bool:
        try:
            await self.client.stat_object(
                bucket_name=bucket_name,
                object_name=object_name,
                **kwargs,
            )
        except miniopy_async.S3Error as error:
            if error.code in (
                settings.MINIO.ERRORS.NO_SUCH_FILE,
                settings.MINIO.ERRORS.NO_SUCH_BUCKET,
            ):
                return False
            raise error
        return True

    async def get_presigned_url(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> str:
        return await self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            **kwargs,
        )
