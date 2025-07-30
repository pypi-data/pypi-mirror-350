from ed_domain.core.entities import Bill
from ed_domain.core.repositories.abc_bill_repository import ABCBillRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class BillRepository(GenericRepository[Bill], ABCBillRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "bill")
