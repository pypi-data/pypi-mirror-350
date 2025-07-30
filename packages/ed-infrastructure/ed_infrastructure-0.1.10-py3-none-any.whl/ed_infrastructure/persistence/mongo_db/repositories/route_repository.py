from ed_domain.core.entities.route import Route
from ed_domain.core.repositories.abc_route_repository import ABCRouteRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class RouteRepository(GenericRepository[Route], ABCRouteRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "route")
