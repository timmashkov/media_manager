from sqlalchemy import UUID, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class File(Base):

    name: Mapped[str] = mapped_column(Text, nullable=False, comment="File's name")
    reference: Mapped[str] = mapped_column(
        Text, index=True, nullable=True, comment="File's reference"
    )
    reference_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), index=True, nullable=True, comment="Reference's uuid"
    )
    bucket: Mapped[str] = mapped_column(Text, nullable=False, comment="File's bucket")
    path: Mapped[str] = mapped_column(Text, nullable=False, comment="File's path")
    mimetype: Mapped[str] = mapped_column(
        Text, nullable=False, comment="File's mimetype"
    )
    jdata: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
        server_default=text("'{}'::jsonb"),
        comment="File's mimetype",
    )
    tags: Mapped[dict] = mapped_column(
        JSONB, nullable=True, server_default=text("'{}'::jsonb"), comment="File's tags"
    )
