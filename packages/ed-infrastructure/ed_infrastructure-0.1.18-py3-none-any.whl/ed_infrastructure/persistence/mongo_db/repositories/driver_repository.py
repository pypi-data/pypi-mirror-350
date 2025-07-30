from ed_domain.core.entities import Driver
from ed_domain.core.repositories.abc_driver_repository import \
    ABCDriverRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class DriverRepository(GenericRepository[Driver], ABCDriverRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "driver")
