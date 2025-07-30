from ed_domain.documentation.common.base_endpoint import BaseEndpoint
from ed_domain.documentation.common.endpoint_description import \
    EndpointDescription
from ed_domain.documentation.common.http_method import HttpMethod

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
                                                      PickUpOrderVerifyDto)
from ed_core.application.features.driver.dtos.update_driver_dto import (
    UpdateDriverDto, UpdateLocationDto)


class CoreEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            # Business endpoints
            {
                "name": "get_all_businesses",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses",
                "response_model": list[BusinessDto],
            },
            {
                "name": "create_business",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses",
                "request_model": CreateBusinessDto,
                "response_model": BusinessDto,
            },
            {
                "name": "get_business",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}",
                "path_params": {"business_id": str},
                "response_model": BusinessDto,
            },
            {
                "name": "update_business",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/businesses/{{business_id}}",
                "path_params": {"business_id": str},
                "request_model": UpdateBusinessDto,
                "response_model": BusinessDto,
            },
            {
                "name": "get_business_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": BusinessDto,
            },
            {
                "name": "get_business_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}/orders",
                "path_params": {"business_id": str},
                "response_model": list[OrderDto],
            },
            {
                "name": "create_business_orders",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses/{{business_id}}/orders",
                "path_params": {"business_id": str},
                "request_model": CreateOrdersDto,
                "response_model": OrderDto,
            },
            # Driver endpoints
            {
                "name": "get_drivers",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers",
                "response_model": list[DriverDto],
            },
            {
                "name": "create_driver",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers",
                "request_model": CreateDriverDto,
                "response_model": DriverDto,
            },
            {
                "name": "get_driver_delivery_jobs",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs",
                "path_params": {"driver_id": str},
                "response_model": list[DeliveryJobDto],
            },
            {
                "name": "get_driver_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/orders",
                "path_params": {"driver_id": str},
                "response_model": list[OrderDto],
            },
            {
                "name": "get_driver",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}",
                "path_params": {"driver_id": str},
                "response_model": DriverDto,
            },
            {
                "name": "update_driver",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/drivers/{{driver_id}}",
                "path_params": {"driver_id": str},
                "request_model": UpdateDriverDto,
                "response_model": DriverDto,
            },
            {
                "name": "update_driver_current_location",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/drivers/{{driver_id}}/current-location",
                "path_params": {"driver_id": str},
                "request_model": UpdateLocationDto,
                "response_model": DriverDto,
            },
            {
                "name": "get_driver_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": DriverDto,
            },
            {
                "name": "claim_delivery_job",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/claim",
                "path_params": {"driver_id": str, "delivery_job_id": str},
                "response_model": DeliveryJobDto,
            },
            {
                "name": "cancel_delivery_job",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/cancel",
                "path_params": {"driver_id": str, "delivery_job_id": str},
                "response_model": DeliveryJobDto,
            },
            {
                "name": "initiate_order_pick_up",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/pick-up",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
                "response_model": PickUpOrderDto,
            },
            {
                "name": "verify_order_pick_up",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/pick-up/verify",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
                "request_model": PickUpOrderVerifyDto,
            },
            {
                "name": "initiate_order_drop_off",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/drop-off",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
                "response_model": DropOffOrderDto,
            },
            {
                "name": "verify_order_drop_off",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/pick-up/verify",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
                "request_model": DropOffOrderVerifyDto,
            },
            {
                "name": "get_driver_payment_summary",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/payment/summary",
                "path_params": {"driver_id": str},
                "response_model": DriverPaymentSummaryDto,
            },
            {
                "name": "get_driver_held_funds",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/payment/held-funds",
                "path_params": {"driver_id": str},
                "response_model": DriverHeldFundsDto,
            },
            # Delivery job endpoints
            {
                "name": "get_delivery_jobs",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/delivery-jobs",
                "response_model": list[DeliveryJobDto],
            },
            {
                "name": "get_delivery_job",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/delivery-jobs/{{delivery_job_id}}",
                "path_params": {"delivery_job_id": str},
                "response_model": DeliveryJobDto,
            },
            {
                "name": "create_delivery_job",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/delivery-jobs",
                "request_model": CreateDeliveryJobDto,
                "response_model": DeliveryJobDto,
            },
            # Order endpoints
            {
                "name": "get_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/orders",
                "response_model": list[OrderDto],
            },
            {
                "name": "get_order",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/orders/{{order_id}}",
                "path_params": {"order_id": str},
                "response_model": OrderDto,
            },
            {
                "name": "track_order",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/orders/{{order_id}}/track",
                "path_params": {"order_id": str},
                "response_model": TrackOrderDto,
            },
            {
                "name": "cancel_order",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/orders/{{order_id}}/cancel",
                "path_params": {"order_id": str},
                "response_model": OrderDto,
            },
            # Consumer endpoints
            {
                "name": "get_consumers",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers",
                "response_model": list[ConsumerDto],
            },
            {
                "name": "create_consumer",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/consumers",
                "request_model": CreateConsumerDto,
                "response_model": ConsumerDto,
            },
            {
                "name": "update_consumer",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/consumers/{{consumer_id}}",
                "path_params": {"consumer_id": str},
                "request_model": UpdateConsumerDto,
                "response_model": ConsumerDto,
            },
            {
                "name": "get_consumer_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers/{{consumer_id}}/orders",
                "path_params": {"consumer_id": str},
                "response_model": list[OrderDto],
            },
            {
                "name": "get_consumer",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers/{{consumer_id}}",
                "path_params": {"consumer_id": str},
                "response_model": ConsumerDto,
            },
            {
                "name": "get_consumer_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": ConsumerDto,
            },
            # Notification features
            {
                "name": "get_user_notifications",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/notifications/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": list[NotificationDto],
            },
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions
