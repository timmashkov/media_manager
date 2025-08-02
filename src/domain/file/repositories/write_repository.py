from typing import Any, Tuple

from sqlalchemy import update

from infrastructure.adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.database.models import File
from infrastructure.database.repositories.write_repository import WriteRepository


class FileWriteRepository(WriteRepository[File]):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        super().__init__(session_adapter, File)

    async def update_item(self, **kwargs: Any) -> Tuple[str, str, dict]:
        uuid = kwargs.pop("uuid")
        async with self._session() as session:
            query = (
                update(self._model)
                .values(**kwargs)
                .where(self._model.uuid == uuid)
                .returning(self._model.name, self._model.bucket, self._model.tags)
            )
            answer = await session.execute(query)
            await session.commit()
            result = answer.fetchone()
        return result.bucket, result.name, result.tags
