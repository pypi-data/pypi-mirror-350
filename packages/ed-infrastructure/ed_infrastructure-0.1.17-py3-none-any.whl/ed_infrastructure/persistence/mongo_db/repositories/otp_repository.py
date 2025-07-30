from ed_domain.core.entities.otp import Otp
from ed_domain.core.repositories.abc_otp_repository import ABCOtpRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class OtpRepository(GenericRepository[Otp], ABCOtpRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "otp")
