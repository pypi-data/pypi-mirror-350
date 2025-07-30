from ed_domain.core.entities import Business
from ed_domain.core.repositories.abc_business_repository import \
    ABCBusinessRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class BusinessRepository(GenericRepository[Business], ABCBusinessRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "business")
