from ed_domain.core.entities.notification import Notification
from ed_domain.core.repositories.abc_notification_repository import \
    ABCNotificationRepository

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories.generic_repository import \
    GenericRepository


class NotificationRepository(
    GenericRepository[Notification], ABCNotificationRepository
):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "notification")
