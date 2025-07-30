from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")


class DbModel(
    Generic[TEntity],
    metaclass=ABCMeta,
):
    @classmethod
    @abstractmethod
    def from_entity(cls, entity: TEntity) -> "DbModel": ...

    @staticmethod
    @abstractmethod
    def to_entity(model: "DbModel") -> TEntity: ...
