import abc
import typing


class FileReaderProtocol(typing.Protocol):
    def read(self) -> bytes:
        pass


class FileAdapterInterface(abc.ABC):
    @abc.abstractmethod
    async def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        data: FileReaderProtocol,
        **kwargs: typing.Any,
    ) -> str:
        pass

    @abc.abstractmethod
    async def download_file_raw(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> typing.Any:
        pass

    @abc.abstractmethod
    async def download_file(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> bytes:
        pass

    @abc.abstractmethod
    async def download_file_chunk(
        self,
        bucket_name: str,
        object_name: str,
        **kwargs: typing.Any,
    ) -> typing.AsyncGenerator[bytes, None]:
        pass

    async def delete_object(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> None:
        pass

    @abc.abstractmethod
    async def get_list_objects(
        self, bucket_name: str, **kwargs: typing.Any
    ) -> typing.Iterator:
        pass

    @abc.abstractmethod
    async def check_file_exist(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> bool:
        pass

    @abc.abstractmethod
    async def get_presigned_url(
        self, bucket_name: str, object_name: str, **kwargs: typing.Any
    ) -> str:
        pass
