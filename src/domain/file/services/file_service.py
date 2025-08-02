from fastapi import UploadFile

from domain.file.entities.dto import FileMetadata
from domain.file.entities.enum import ContentType
from domain.file.entities.model import FileIncomingData


class FileService:

    @staticmethod
    def _build_valid_path(path: str, name: str, extension: str) -> str:
        return f"{path}/{name}.{extension}"

    @staticmethod
    def _build_valid_name(name: str, extension: str) -> str:
        valid_name = (
            name + extension if extension.startswith(".") else name + "." + extension
        )
        return valid_name

    @staticmethod
    def _build_valid_extension(file: UploadFile, model_extension: str) -> str:
        file_extension = file.filename.split(".")[-1]
        if file_extension == model_extension:
            return model_extension
        return file_extension

    @staticmethod
    def _build_content_type(extension: str) -> str:
        content_types = ContentType.to_dict()
        if extension.upper() in content_types.keys():
            return content_types.get(extension.upper())
        raise ValueError("Wrong extension found")

    @staticmethod
    def _build_valid_metadata(
        valid_name: str,
        valid_path: str,
        bucket: str,
        valid_extension: str,
        valid_content_type: str,
    ) -> FileMetadata:
        return FileMetadata(
            object_name=valid_name,
            full_path=valid_path,
            bucket=bucket,
            content_type=valid_extension,
            extension=valid_content_type,
        )

    @staticmethod
    def _build_valid_api_model(
        api_model: FileIncomingData,
        valid_name: str,
        valid_path: str,
        valid_content_type: str,
    ) -> FileIncomingData:
        raw_model = api_model.model_dump()
        raw_model["name"] = valid_name
        raw_model["path"] = valid_path
        raw_model["mimetype"] = valid_content_type
        return FileIncomingData(**raw_model)

    def build_valid_data(
        self, income_data: FileIncomingData, file: UploadFile
    ) -> tuple[FileMetadata, FileIncomingData]:
        valid_extension = self._build_valid_extension(
            file=file, model_extension=income_data.mimetype
        )
        valid_path = self._build_valid_path(
            path=income_data.bucket, name=income_data.name, extension=valid_extension
        )
        valid_name = self._build_valid_name(
            name=income_data.name, extension=valid_extension
        )
        valid_content_type = self._build_content_type(extension=valid_extension)
        file_metadata = self._build_valid_metadata(
            valid_name=valid_name,
            valid_path=valid_path,
            bucket=income_data.bucket,
            valid_extension=valid_extension,
            valid_content_type=valid_content_type,
        )
        api_model = self._build_valid_api_model(
            api_model=income_data,
            valid_name=valid_name,
            valid_path=valid_path,
            valid_content_type=valid_content_type,
        )
        return file_metadata, api_model
