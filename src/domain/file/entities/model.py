import datetime
import typing
from uuid import UUID

import orjson
import pydantic

from infrastructure.common.base_entities.patched_filter import PatchedFilter
from infrastructure.database.models import File


class FileIncomingData(pydantic.BaseModel):

    name: str = pydantic.Field(description=File.name.comment)
    path: str = pydantic.Field(description=File.path.comment)
    tags: dict | None = pydantic.Field(
        default_factory=dict, description=File.tags.comment
    )
    jdata: dict | None = pydantic.Field(
        default_factory=dict, description=File.jdata.comment
    )
    references: str | None = pydantic.Field(
        default=None, description=File.reference.comment
    )
    reference_uuid: UUID | None = pydantic.Field(
        default=None, description=File.reference_uuid.comment
    )
    bucket: str = pydantic.Field(description=File.bucket.comment)
    mimetype: str = pydantic.Field(description=File.mimetype.comment)

    @classmethod
    @pydantic.model_validator(mode="before")
    def validate_to_json(cls, value: dict | str) -> typing.Any:
        if isinstance(value, str):
            return orjson.loads(value)
        return value


class FileResultData(FileIncomingData):
    uuid: UUID = pydantic.Field(description=File.uuid.comment)
    created_at: datetime.datetime = pydantic.Field(description=File.created_at.comment)
    updated_at: datetime.datetime = pydantic.Field(description=File.updated_at.comment)


class FileFilter(PatchedFilter):
    uuid: UUID | None = None
    name: str | None = None

    class Constants(PatchedFilter.Constants):
        model = File
