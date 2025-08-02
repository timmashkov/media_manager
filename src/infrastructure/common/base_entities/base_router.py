from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_filter.base.filter import BaseFilterModel
from pydantic import BaseModel

from infrastructure.common.exceptions.api_axceptions import RouterInitializationError
from infrastructure.common.interfaces.use_case_interface import UseCaseInterface


class BaseRouter:
    prefix: str
    tags: list[str]
    api_router: APIRouter
    filters: type[BaseFilterModel]
    service_client: UseCaseInterface
    input_model: BaseModel
    output_model: BaseModel

    def __init__(self) -> None:
        self._arguments: tuple = (
            self.filters,
            self.input_model,
            self.output_model,
            self.service_client,
        )
        self.__init_router()
        self._add_routes()

    def __init_router(self) -> None:
        if all(self._arguments):
            self.api_router = APIRouter(prefix=self.prefix, tags=self.tags)
            self.filters = FilterDepends(self.filters)
            self.service_instance = self.service_client
            return
        raise RouterInitializationError

    def _add_routes(self) -> None:
        _filters = self.filters
        _input_model = self.input_model
        _output_model = self.output_model
        _service_instance = self.service_instance

        @self.api_router.get(
            "/{uuid}",
            response_model=_output_model,
            name=f"get_{self.prefix[1:]}",
            operation_id=f"get_{self.prefix}_by_uuid",
        )
        async def get_object(
            uuid: str | UUID, service_instance: _service_instance = Depends()
        ):
            return await service_instance.get_item(uuid)

        @self.api_router.get(
            "/",
            response_model=List[_output_model],
            name=f"get_{self.prefix[1:]}s",
            operation_id=f"get_{self.prefix}_list",
        )
        async def get_objects(
            filters: _filters = _filters,
            service_instance: _service_instance = Depends(),
        ):
            return await service_instance.get_items(filters=filters)

        @self.api_router.post(
            "/",
            response_model=_output_model,
            name=f"create_{self.prefix[1:]}",
            operation_id=f"create_{self.prefix[1:]}",
        )
        async def create_object(
            data: _input_model, service_instance: _service_instance = Depends()
        ):
            return await service_instance.create_item(data)

        @self.api_router.patch(
            "/{uuid}",
            response_model=_output_model,
            name=f"update_{self.prefix[1:]}",
            operation_id=f"update_{self.prefix[1:]}",
        )
        async def update_object(
            uuid: str | UUID,
            data: _input_model,
            service_instance: _service_instance = Depends(),
        ):
            return await service_instance.update_item(uuid, data)

        @self.api_router.delete(
            "/{uuid}",
            response_model=_output_model,
            name=f"delete_{self.prefix[1:]}",
            operation_id=f"delete_{self.prefix[1:]}",
        )
        async def delete_object(
            uuid: str | UUID, service_instance: _service_instance = Depends()
        ):
            return await service_instance.delete_item(uuid)
