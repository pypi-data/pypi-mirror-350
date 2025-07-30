from abc import ABCMeta, abstractmethod

from ed_domain.core.repositories.abc_auth_user_repository import \
    ABCAuthUserRepository
from ed_domain.core.repositories.abc_bill_repository import ABCBillRepository
from ed_domain.core.repositories.abc_business_repository import \
    ABCBusinessRepository
from ed_domain.core.repositories.abc_car_repository import ABCCarRepository
from ed_domain.core.repositories.abc_consumer_repository import \
    ABCConsumerRepository
from ed_domain.core.repositories.abc_delivery_job_repository import \
    ABCDeliveryJobRepository
from ed_domain.core.repositories.abc_driver_repository import \
    ABCDriverRepository
from ed_domain.core.repositories.abc_location_repository import \
    ABCLocationRepository
from ed_domain.core.repositories.abc_notification_repository import \
    ABCNotificationRepository
from ed_domain.core.repositories.abc_order_repository import ABCOrderRepository
from ed_domain.core.repositories.abc_otp_repository import ABCOtpRepository
from ed_domain.core.repositories.abc_route_repository import ABCRouteRepository


class ABCUnitOfWork(metaclass=ABCMeta):
    @property
    @abstractmethod
    def bill_repository(self) -> ABCBillRepository: ...

    @property
    @abstractmethod
    def business_repository(self) -> ABCBusinessRepository: ...

    @property
    @abstractmethod
    def car_repository(self) -> ABCCarRepository: ...

    @property
    @abstractmethod
    def consumer_repository(self) -> ABCConsumerRepository: ...

    @property
    @abstractmethod
    def delivery_job_repository(self) -> ABCDeliveryJobRepository: ...

    @property
    @abstractmethod
    def driver_repository(self) -> ABCDriverRepository: ...

    @property
    @abstractmethod
    def location_repository(self) -> ABCLocationRepository: ...

    @property
    @abstractmethod
    def notification_repository(self) -> ABCNotificationRepository: ...

    @property
    @abstractmethod
    def order_repository(self) -> ABCOrderRepository: ...

    @property
    @abstractmethod
    def otp_repository(self) -> ABCOtpRepository: ...

    @property
    @abstractmethod
    def route_repository(self) -> ABCRouteRepository: ...

    @property
    @abstractmethod
    def auth_user_repository(self) -> ABCAuthUserRepository: ...
