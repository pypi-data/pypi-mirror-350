from ed_domain.core.entities.auth_user import AuthUser
from ed_domain.core.repositories.abc_auth_user_repository import \
    ABCAuthUserRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class AuthUserRepository(GenericRepository[AuthUser], ABCAuthUserRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "user")
