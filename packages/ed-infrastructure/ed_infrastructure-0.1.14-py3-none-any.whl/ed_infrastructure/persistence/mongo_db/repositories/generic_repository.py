from typing import Any, Generic, TypeVar
from uuid import UUID

from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository

from ed_infrastructure.persistence.helpers import repository_class
from ed_infrastructure.persistence.mongo_db.db_client import DbClient

TEntity = TypeVar("TEntity")


@repository_class
class GenericRepository(ABCGenericRepository[TEntity], Generic[TEntity]):
    def __init__(self, db: DbClient, collection: str) -> None:
        self._db = db.get_collection(f"{collection}s")
        self._collection = f"{collection[0].upper()}{collection[1:].lower()}"

    def get_all(self, **filters: Any) -> list[TEntity]:
        return list(self._db.find(filters))

    def get(self, **filters: Any) -> TEntity | None:
        if entity := self._db.find_one(filters):
            return entity

        return None

    def create(self, entity: TEntity) -> TEntity:
        self._db.insert_one(entity)
        return entity

    def create_many(self, entities: list[TEntity]) -> list[TEntity]:
        self._db.insert_many(entities)
        return entities

    def update(self, id: UUID, entity: TEntity) -> bool:
        status = self._db.update_one({"id": id}, {"$set": entity})
        return status.modified_count > 0

    def delete(self, id: UUID) -> bool:
        status = self._db.delete_one({"id": id})
        return status.deleted_count > 0
