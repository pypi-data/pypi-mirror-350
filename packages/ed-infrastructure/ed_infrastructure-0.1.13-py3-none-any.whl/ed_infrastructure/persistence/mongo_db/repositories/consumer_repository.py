from ed_domain.core.entities import Consumer
from ed_domain.core.repositories.abc_consumer_repository import \
    ABCConsumerRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class ConsumerRepository(GenericRepository[Consumer], ABCConsumerRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "consumer")
