from ed_domain.core.repositories import (ABCAuthUserRepository,
                                         ABCBillRepository,
                                         ABCBusinessRepository,
                                         ABCCarRepository,
                                         ABCConsumerRepository,
                                         ABCDeliveryJobRepository,
                                         ABCDriverRepository,
                                         ABCLocationRepository,
                                         ABCNotificationRepository,
                                         ABCOrderRepository, ABCOtpRepository,
                                         ABCRouteRepository, ABCUnitOfWork)

from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.repositories import (
    AuthUserRepository, BillRepository, BusinessRepository, CarRepository,
    ConsumerRepository, DeliveryJobRepository, DriverRepository,
    LocationRepository, NotificationRepository, OrderRepository, OtpRepository,
    RouteRepository)


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, db_client: DbClient) -> None:
        self._bill_repository = BillRepository(db_client)
        self._business_repository = BusinessRepository(db_client)
        self._car_repository = CarRepository(db_client)
        self._consumer_repository = ConsumerRepository(db_client)
        self._delivery_job_repository = DeliveryJobRepository(db_client)
        self._driver_repository = DriverRepository(db_client)
        self._location_repository = LocationRepository(db_client)
        self._notification_repository = NotificationRepository(db_client)
        self._order_repository = OrderRepository(db_client)
        self._otp_repository = OtpRepository(db_client)
        self._route_repository = RouteRepository(db_client)
        self._auth_user_repository = AuthUserRepository(db_client)

    @property
    def bill_repository(self) -> ABCBillRepository:
        return self._bill_repository

    @property
    def business_repository(self) -> ABCBusinessRepository:
        return self._business_repository

    @property
    def car_repository(self) -> ABCCarRepository:
        return self._car_repository

    @property
    def consumer_repository(self) -> ABCConsumerRepository:
        return self._consumer_repository

    @property
    def delivery_job_repository(self) -> ABCDeliveryJobRepository:
        return self._delivery_job_repository

    @property
    def driver_repository(self) -> ABCDriverRepository:
        return self._driver_repository

    @property
    def location_repository(self) -> ABCLocationRepository:
        return self._location_repository

    @property
    def notification_repository(self) -> ABCNotificationRepository:
        return self._notification_repository

    @property
    def order_repository(self) -> ABCOrderRepository:
        return self._order_repository

    @property
    def otp_repository(self) -> ABCOtpRepository:
        return self._otp_repository

    @property
    def route_repository(self) -> ABCRouteRepository:
        return self._route_repository

    @property
    def auth_user_repository(self) -> ABCAuthUserRepository:
        return self._auth_user_repository
