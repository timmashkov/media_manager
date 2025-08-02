import datetime
from uuid import UUID

import orjson
import pydantic
from fastapi import Form

from infrastructure.common.base_entities.patched_filter import PatchedFilter
from infrastructure.database.models import File


class FileBaseData(pydantic.BaseModel):

    bucket: str = pydantic.Field(description=File.bucket.comment)
    name: str = pydantic.Field(description=File.name.comment)

class FileIncomingData(FileBaseData):

    path: str = pydantic.Field(description=File.path.comment)
    tags: dict | None = pydantic.Field(default_factory=dict)
    jdata: dict | None = pydantic.Field(default_factory=dict)
    reference: str | None = pydantic.Field(
        default=None, description=File.reference.comment
    )
    reference_uuid: UUID | None = pydantic.Field(
        default=None, description=File.reference_uuid.comment
    )

    mimetype: str = pydantic.Field(description=File.mimetype.comment)

    @classmethod
    def from_form(
        cls,
        name: str = Form(...),
        path: str = Form(...),
        tags: str = Form("{}"),
        jdata: str = Form("{}"),
        reference: str | None = Form(None),
        reference_uuid: UUID | None = Form(None),
        bucket: str = Form(...),
        mimetype: str = Form(...),
    ):
        return cls(
            name=name,
            path=path,
            tags=orjson.loads(tags),
            jdata=orjson.loads(jdata),
            reference=reference,
            reference_uuid=reference_uuid,
            bucket=bucket,
            mimetype=mimetype,
        )


class FileResultData(FileIncomingData):
    uuid: UUID = pydantic.Field(description=File.uuid.comment)
    created_at: datetime.datetime = pydantic.Field(description=File.created_at.comment)
    updated_at: datetime.datetime = pydantic.Field(description=File.updated_at.comment)


class FileFilter(PatchedFilter):
    uuid: UUID | None = None
    name: str | None = None

    class Constants(PatchedFilter.Constants):
        model = File
