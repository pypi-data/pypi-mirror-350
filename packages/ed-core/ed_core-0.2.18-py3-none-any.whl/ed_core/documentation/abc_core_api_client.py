from abc import ABCMeta, abstractmethod

from ed_domain.documentation.common.api_response import ApiResponse

from ed_core.application.features.business.dtos import (CreateBusinessDto,
                                                        CreateOrdersDto,
                                                        UpdateBusinessDto)
from ed_core.application.features.common.dtos import (BillDto, BusinessDto,
                                                      ConsumerDto,
                                                      DeliveryJobDto,
                                                      DriverDto,
                                                      NotificationDto,
                                                      OrderDto, TrackOrderDto)
from ed_core.application.features.consumer.dtos import (CreateConsumerDto,
                                                        UpdateConsumerDto)
from ed_core.application.features.delivery_job.dtos import CreateDeliveryJobDto
from ed_core.application.features.driver.dtos import (CreateDriverDto,
                                                      DriverHeldFundsDto,
                                                      DriverPaymentSummaryDto,
                                                      DropOffOrderDto,
                                                      DropOffOrderVerifyDto,
                                                      PickUpOrderDto,
                                                      PickUpOrderVerifyDto,
                                                      UpdateDriverDto)
from ed_core.application.features.driver.dtos.update_driver_dto import \
    UpdateLocationDto


class ABCCoreApiClient(metaclass=ABCMeta):
    # Driver features
    @abstractmethod
    def get_drivers(self) -> ApiResponse[list[DriverDto]]: ...

    @abstractmethod
    def create_driver(
        self, create_driver_dto: CreateDriverDto
    ) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def get_driver_orders(
        self, driver_id: str) -> ApiResponse[list[OrderDto]]: ...

    @abstractmethod
    def get_driver_delivery_jobs(
        self, driver_id: str
    ) -> ApiResponse[list[DeliveryJobDto]]: ...

    @abstractmethod
    def get_driver(self, driver_id: str) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def get_driver_held_funds(
        self, driver_id: str
    ) -> ApiResponse[DriverHeldFundsDto]: ...

    @abstractmethod
    def get_driver_payment_summary(
        self, driver_id: str
    ) -> ApiResponse[DriverPaymentSummaryDto]: ...

    @abstractmethod
    def update_driver(
        self, driver_id: str, update_driver_dto: UpdateDriverDto
    ) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def update_driver_current_location(
        self, driver_id: str, update_location_dto: UpdateLocationDto
    ) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def get_driver_by_user_id(
        self, user_id: str) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def claim_delivery_job(
        self, driver_id: str, delivery_job_id: str
    ) -> ApiResponse[DeliveryJobDto]: ...

    @abstractmethod
    def cancel_delivery_job(
        self, driver_id: str, delivery_job_id: str
    ) -> ApiResponse[DeliveryJobDto]: ...

    @abstractmethod
    def initiate_order_pick_up(
        self, driver_id: str, delivery_job_id: str, order_id: str
    ) -> ApiResponse[PickUpOrderDto]: ...

    @abstractmethod
    def verify_order_pick_up(
        self,
        driver_id: str,
        delivery_job_id: str,
        order_id: str,
        pick_up_order_verify_dto: PickUpOrderVerifyDto,
    ) -> ApiResponse[None]: ...

    @abstractmethod
    def initiate_order_drop_off(
        self, driver_id: str, delivery_job_id: str, order_id: str
    ) -> ApiResponse[DropOffOrderDto]: ...

    @abstractmethod
    def verify_order_drop_off(
        self,
        driver_id: str,
        delivery_job_id: str,
        order_id: str,
        drop_off_order_verify_dto: DropOffOrderVerifyDto,
    ) -> ApiResponse[None]: ...

    # Business features
    @abstractmethod
    def get_all_businesses(self) -> ApiResponse[list[BusinessDto]]: ...

    @abstractmethod
    def create_business(
        self, create_business_dto: CreateBusinessDto
    ) -> ApiResponse[BusinessDto]: ...

    @abstractmethod
    def get_business(self, business_id: str) -> ApiResponse[BusinessDto]: ...

    @abstractmethod
    def update_business(
        self, business_id: str, update_business_dto: UpdateBusinessDto
    ) -> ApiResponse[BusinessDto]: ...

    @abstractmethod
    def get_business_by_user_id(
        self, user_id: str) -> ApiResponse[BusinessDto]: ...

    @abstractmethod
    def get_business_orders(
        self, business_id: str) -> ApiResponse[list[OrderDto]]: ...

    @abstractmethod
    def create_business_orders(
        self, business_id: str, create_orders_dto: CreateOrdersDto
    ) -> ApiResponse[list[OrderDto]]: ...

    # Delivery job features
    @abstractmethod
    def get_delivery_jobs(self) -> ApiResponse[list[DeliveryJobDto]]: ...

    @abstractmethod
    def get_delivery_job(
        self, delivery_job_id: str) -> ApiResponse[DeliveryJobDto]: ...

    @abstractmethod
    def create_delivery_job(
        self, create_delivery_job_dto: CreateDeliveryJobDto
    ) -> ApiResponse[DeliveryJobDto]: ...

    # Order features
    @abstractmethod
    def get_orders(self) -> ApiResponse[list[OrderDto]]: ...

    @abstractmethod
    def track_order(self, order_id: str) -> ApiResponse[TrackOrderDto]: ...

    @abstractmethod
    def get_order(self, order_id: str) -> ApiResponse[OrderDto]: ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> ApiResponse[OrderDto]: ...

    # Consumer features
    @abstractmethod
    def get_consumers(self) -> ApiResponse[list[ConsumerDto]]: ...

    @abstractmethod
    def create_consumer(
        self, create_consumer_dto: CreateConsumerDto
    ) -> ApiResponse[ConsumerDto]: ...

    @abstractmethod
    def get_consumer_delivery_jobs(
        self, consumer_id: str
    ) -> ApiResponse[list[OrderDto]]: ...

    @abstractmethod
    def get_consumer(self, consumer_id: str) -> ApiResponse[ConsumerDto]: ...

    @abstractmethod
    def update_consumer(
        self, consumer_id: str, update_consumer_dto: UpdateConsumerDto
    ) -> ApiResponse[ConsumerDto]: ...

    @abstractmethod
    def get_consumer_by_user_id(
        self, user_id: str) -> ApiResponse[ConsumerDto]: ...

    # Notification featuers
    @abstractmethod
    def get_user_notifications(
        self, user_id: str
    ) -> ApiResponse[list[NotificationDto]]: ...
