from dataclasses import asdict, dataclass
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def dto_to_pydantic(dto: dataclass, pydantic_model: Type[T]) -> T:
    """Конвертирует любой dataclass DTO в Pydantic модель."""
    return pydantic_model(**asdict(dto))
