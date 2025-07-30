from ed_domain.documentation.common.api_response import ApiResponse
from ed_infrastructure.utils.api.api_client import ApiClient

from ed_core.application.features.business.dtos import (CreateBusinessDto,
                                                        CreateOrdersDto,
                                                        UpdateBusinessDto)
from ed_core.application.features.common.dtos import (BusinessDto, ConsumerDto,
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
from ed_core.documentation.abc_core_api_client import ABCCoreApiClient
from ed_core.documentation.endpoints import CoreEndpoint


class CoreApiClient(ABCCoreApiClient):
    def __init__(self, core_api: str) -> None:
        self._endpoints = CoreEndpoint(core_api)

    def get_drivers(self) -> ApiResponse[list[DriverDto]]:
        endpoint = self._endpoints.get_description("get_drivers")
        api_client = ApiClient[list[DriverDto]](endpoint)

        return api_client({})

    def create_driver(
        self, create_driver_dto: CreateDriverDto
    ) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("create_driver")
        api_client = ApiClient[DriverDto](endpoint)

        return api_client({"request": create_driver_dto})

    def get_driver_orders(self, driver_id: str) -> ApiResponse[list[OrderDto]]:
        endpoint = self._endpoints.get_description("get_driver_orders")
        api_client = ApiClient[list[OrderDto]](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def get_driver_delivery_jobs(
        self, driver_id: str
    ) -> ApiResponse[list[DeliveryJobDto]]:
        endpoint = self._endpoints.get_description("get_driver_delivery_jobs")
        api_client = ApiClient[list[DeliveryJobDto]](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def get_driver_by_user_id(self, user_id: str) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("get_driver_by_user_id")
        api_client = ApiClient[DriverDto](endpoint)
        return api_client({"path_params": {"user_id": user_id}})

    def get_driver_held_funds(self, driver_id: str) -> ApiResponse[DriverHeldFundsDto]:
        endpoint = self._endpoints.get_description("get_driver_held_funds")
        api_client = ApiClient[DriverHeldFundsDto](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def get_driver_payment_summary(
        self, driver_id: str
    ) -> ApiResponse[DriverPaymentSummaryDto]:
        endpoint = self._endpoints.get_description(
            "get_driver_payment_summary")
        api_client = ApiClient[DriverPaymentSummaryDto](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def get_driver(self, driver_id: str) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("get_driver")
        api_client = ApiClient[DriverDto](endpoint)
        return api_client({"path_params": {"driver_id": driver_id}})

    def update_driver(
        self, driver_id: str, update_driver_dto: UpdateDriverDto
    ) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description("update_driver")
        api_client = ApiClient[DriverDto](endpoint)
        return api_client(
            {"path_params": {"driver_id": driver_id}, "request": update_driver_dto}
        )

    def update_driver_current_location(
        self, driver_id: str, update_location_dto: UpdateLocationDto
    ) -> ApiResponse[DriverDto]:
        endpoint = self._endpoints.get_description(
            "update_driver_current_location")
        api_client = ApiClient[DriverDto](endpoint)
        return api_client(
            {"path_params": {"driver_id": driver_id},
                "request": update_location_dto}
        )

    def claim_delivery_job(
        self, driver_id: str, delivery_job_id: str
    ) -> ApiResponse[DeliveryJobDto]:
        endpoint = self._endpoints.get_description("claim_delivery_job")
        api_client = ApiClient[DeliveryJobDto](endpoint)
        return api_client(
            {
                "path_params": {
                    "driver_id": driver_id,
                    "delivery_job_id": delivery_job_id,
                }
            }
        )

    def cancel_delivery_job(
        self, driver_id: str, delivery_job_id: str
    ) -> ApiResponse[DeliveryJobDto]:
        endpoint = self._endpoints.get_description("cancel_delivery_job")
        api_client = ApiClient[DeliveryJobDto](endpoint)
        return api_client(
            {
                "path_params": {
                    "driver_id": driver_id,
                    "delivery_job_id": delivery_job_id,
                }
            }
        )

    def initiate_order_pick_up(
        self, driver_id: str, delivery_job_id: str, order_id: str
    ) -> ApiResponse[PickUpOrderDto]:
        endpoint = self._endpoints.get_description("initiate_order_pick_up")
        api_client = ApiClient[PickUpOrderDto](endpoint)
        return api_client(
            {
                "path_params": {
                    "driver_id": driver_id,
                    "delivery_job_id": delivery_job_id,
                    "order_id": order_id,
                }
            }
        )

    def verify_order_pick_up(
        self,
        driver_id: str,
        delivery_job_id: str,
        order_id: str,
        pick_up_order_verify_dto: PickUpOrderVerifyDto,
    ) -> ApiResponse[None]:
        endpoint = self._endpoints.get_description("verify_order_pick_up")
        api_client = ApiClient[None](endpoint)
        return api_client(
            {
                "path_params": {
                    "driver_id": driver_id,
                    "delivery_job_id": delivery_job_id,
                    "order_id": order_id,
                },
                "request": pick_up_order_verify_dto,
            }
        )

    def initiate_order_drop_off(
        self, driver_id: str, delivery_job_id: str, order_id: str
    ) -> ApiResponse[DropOffOrderDto]:
        endpoint = self._endpoints.get_description("initiate_order_drop_off")
        api_client = ApiClient[DropOffOrderDto](endpoint)
        return api_client(
            {
                "path_params": {
                    "driver_id": driver_id,
                    "delivery_job_id": delivery_job_id,
                    "order_id": order_id,
                }
            }
        )

    def verify_order_drop_off(
        self,
        driver_id: str,
        delivery_job_id: str,
        order_id: str,
        drop_off_order_verify_dto: DropOffOrderVerifyDto,
    ) -> ApiResponse[None]:
        endpoint = self._endpoints.get_description("verify_order_drop_off")
        api_client = ApiClient[None](endpoint)
        return api_client(
            {
                "path_params": {
                    "driver_id": driver_id,
                    "delivery_job_id": delivery_job_id,
                    "order_id": order_id,
                },
                "request": drop_off_order_verify_dto,
            }
        )

    def get_all_businesses(self) -> ApiResponse[list[BusinessDto]]:
        endpoint = self._endpoints.get_description("get_all_businesses")
        api_client = ApiClient[list[BusinessDto]](endpoint)
        return api_client({})

    def create_business(
        self, create_business_dto: CreateBusinessDto
    ) -> ApiResponse[BusinessDto]:
        endpoint = self._endpoints.get_description("create_business")
        api_client = ApiClient[BusinessDto](endpoint)
        return api_client({"request": create_business_dto})

    def get_business_by_user_id(self, user_id: str) -> ApiResponse[BusinessDto]:
        endpoint = self._endpoints.get_description("get_business_by_user_id")
        api_client = ApiClient[BusinessDto](endpoint)
        return api_client({"path_params": {"user_id": user_id}})

    def get_business(self, business_id: str) -> ApiResponse[BusinessDto]:
        endpoint = self._endpoints.get_description("get_business")
        api_client = ApiClient[BusinessDto](endpoint)
        return api_client({"path_params": {"business_id": business_id}})

    def update_business(
        self, business_id: str, update_business_dto: UpdateBusinessDto
    ) -> ApiResponse[BusinessDto]:
        endpoint = self._endpoints.get_description("updaate_business")
        api_client = ApiClient[BusinessDto](endpoint)
        return api_client(
            {
                "path_params": {"business_id": business_id},
                "request": update_business_dto,
            }
        )

    def get_business_orders(self, business_id: str) -> ApiResponse[list[OrderDto]]:
        endpoint = self._endpoints.get_description("get_business_orders")
        api_client = ApiClient[list[OrderDto]](endpoint)
        return api_client({"path_params": {"business_id": business_id}})

    def create_business_orders(
        self, business_id: str, create_orders_dto: CreateOrdersDto
    ) -> ApiResponse[list[OrderDto]]:
        endpoint = self._endpoints.get_description("create_business_order")
        api_client = ApiClient[list[OrderDto]](endpoint)
        return api_client(
            {"path_params": {"business_id": business_id},
                "request": create_orders_dto}
        )

    def get_delivery_jobs(self) -> ApiResponse[list[DeliveryJobDto]]:
        endpoint = self._endpoints.get_description("get_delivery_jobs")
        api_client = ApiClient[list[DeliveryJobDto]](endpoint)
        return api_client({})

    def get_delivery_job(self, delivery_job_id: str) -> ApiResponse[DeliveryJobDto]:
        endpoint = self._endpoints.get_description("get_delivery_job")
        api_client = ApiClient[DeliveryJobDto](endpoint)
        return api_client({"path_params": {"delivery_job_id": delivery_job_id}})

    def create_delivery_job(
        self, create_delivery_job_dto: CreateDeliveryJobDto
    ) -> ApiResponse[DeliveryJobDto]:
        endpoint = self._endpoints.get_description("create_delivery_job")
        api_client = ApiClient[DeliveryJobDto](endpoint)
        return api_client({"request": create_delivery_job_dto})

    def get_orders(self) -> ApiResponse[list[OrderDto]]:
        endpoint = self._endpoints.get_description("get_orders")
        api_client = ApiClient[list[OrderDto]](endpoint)
        return api_client({})

    def get_order(self, order_id: str) -> ApiResponse[OrderDto]:
        endpoint = self._endpoints.get_description("get_order")
        api_client = ApiClient[OrderDto](endpoint)
        return api_client({"path_params": {"order_id": order_id}})

    def track_order(self, order_id: str) -> ApiResponse[TrackOrderDto]:
        endpoint = self._endpoints.get_description("track_order")
        api_client = ApiClient[TrackOrderDto](endpoint)
        return api_client({"path_params": {"order_id": order_id}})

    def cancel_order(self, order_id: str) -> ApiResponse[OrderDto]:
        endpoint = self._endpoints.get_description("cancel_order")
        api_client = ApiClient[OrderDto](endpoint)
        return api_client({"path_params": {"order_id": order_id}})

    def get_consumers(self) -> ApiResponse[list[ConsumerDto]]:
        endpoint = self._endpoints.get_description("get_consumers")
        api_client = ApiClient[list[ConsumerDto]](endpoint)

        return api_client({})

    def create_consumer(
        self, create_consumer_dto: CreateConsumerDto
    ) -> ApiResponse[ConsumerDto]:
        endpoint = self._endpoints.get_description("create_consumer")
        api_client = ApiClient[ConsumerDto](endpoint)

        return api_client({"request": create_consumer_dto})

    def get_consumer_delivery_jobs(
        self, consumer_id: str
    ) -> ApiResponse[list[OrderDto]]:
        endpoint = self._endpoints.get_description(
            "get_consumer_delivery_jobs")
        api_client = ApiClient[list[OrderDto]](endpoint)
        return api_client({"path_params": {"consumer_id": consumer_id}})

    def get_consumer_by_user_id(self, user_id: str) -> ApiResponse[ConsumerDto]:
        endpoint = self._endpoints.get_description("get_consumer_by_user_id")
        api_client = ApiClient[ConsumerDto](endpoint)
        return api_client({"path_params": {"user_id": user_id}})

    def get_consumer(self, consumer_id: str) -> ApiResponse[ConsumerDto]:
        endpoint = self._endpoints.get_description("get_consumer")
        api_client = ApiClient[ConsumerDto](endpoint)
        return api_client({"path_params": {"consumer_id": consumer_id}})

    def update_consumer(
        self, consumer_id: str, update_consumer_dto: UpdateConsumerDto
    ) -> ApiResponse[ConsumerDto]:
        endpoint = self._endpoints.get_description("update_consumer")
        api_client = ApiClient[ConsumerDto](endpoint)
        return api_client(
            {
                "path_params": {"consumer_id": consumer_id},
                "request": update_consumer_dto,
            }
        )

    def get_user_notifications(
        self, user_id: str
    ) -> ApiResponse[list[NotificationDto]]:
        endpoint = self._endpoints.get_description("get_user_notifications")
        api_client = ApiClient[list[NotificationDto]](endpoint)
        return api_client({"path_params": {"user_id": user_id}})


if __name__ == "__main__":
    CoreApiClient("")
