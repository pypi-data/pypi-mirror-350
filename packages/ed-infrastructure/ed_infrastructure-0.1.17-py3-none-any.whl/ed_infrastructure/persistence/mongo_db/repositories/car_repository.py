from ed_domain.core.entities import Car
from ed_domain.core.repositories.abc_car_repository import ABCCarRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class CarRepository(GenericRepository[Car], ABCCarRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "car")
