from typing import Any, Generic, Iterable, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.common.base_entities.typevars import table
from infrastructure.common.interfaces.repository_interfaces import (
    AbstractReadRepository,
)


class ReadRepository(AbstractReadRepository, Generic[table]):

    def __init__(self, session_adapter: AlchemyAdapter, model: Type[table]) -> None:
        self._model = model
        self._session: async_sessionmaker = session_adapter.autocommit_session

    @classmethod
    def __set_filter(cls, query: select, filters: Any = None) -> select:
        if filters:
            query = filters.filter(query)
        return query

    def _get_query(self) -> select:
        query = select(self._model)
        return query

    async def get_item(self, uuid: str | UUID) -> table | None:
        async with self._session() as session:
            stmt = self._get_query().where(self._model.uuid == uuid)
            answer = await session.execute(stmt)
        return answer.unique().scalar_one_or_none()

    async def find(
        self,
        filters: Any = None,
    ) -> Iterable[table]:
        query = self._get_query()
        query = self.__set_filter(query, filters)
        async with self._session() as session:
            result = await session.execute(query)
            return result.scalars().unique().all()
