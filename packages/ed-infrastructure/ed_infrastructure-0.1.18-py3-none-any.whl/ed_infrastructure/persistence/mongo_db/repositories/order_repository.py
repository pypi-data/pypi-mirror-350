from ed_domain.core.entities.order import Order
from ed_domain.core.repositories.abc_order_repository import ABCOrderRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class OrderRepository(GenericRepository[Order], ABCOrderRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "order")
