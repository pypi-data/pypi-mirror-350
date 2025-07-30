from abc import ABCMeta, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

TEntity = TypeVar("TEntity")


class ABCGenericRepository(Generic[TEntity], metaclass=ABCMeta):
    @abstractmethod
    def get_all(self, **filters: Any) -> list[TEntity]: ...

    @abstractmethod
    def get(self, **filters: Any) -> TEntity | None: ...

    @abstractmethod
    def create(self, entity: TEntity) -> TEntity: ...

    @abstractmethod
    def create_many(self, entities: list[TEntity]) -> list[TEntity]: ...

    @abstractmethod
    def update(self, id: UUID, entity: TEntity) -> bool: ...

    @abstractmethod
    def delete(self, id: UUID) -> bool: ...
