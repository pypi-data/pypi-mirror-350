from ed_domain.core.entities import DeliveryJob
from ed_domain.core.repositories.abc_delivery_job_repository import \
    ABCDeliveryJobRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class DeliveryJobRepository(GenericRepository[DeliveryJob], ABCDeliveryJobRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "delivery_job")
