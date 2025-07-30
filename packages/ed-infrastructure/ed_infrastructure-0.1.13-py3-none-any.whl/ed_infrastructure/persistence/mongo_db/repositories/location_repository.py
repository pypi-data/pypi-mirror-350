from ed_domain.core.entities.location import Location
from ed_domain.core.repositories.abc_location_repository import \
    ABCLocationRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class LocationRepository(GenericRepository[Location], ABCLocationRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "location")
