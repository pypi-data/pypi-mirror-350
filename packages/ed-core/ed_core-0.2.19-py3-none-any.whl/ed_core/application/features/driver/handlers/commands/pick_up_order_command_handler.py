from datetime import UTC, datetime, timedelta
from uuid import UUID

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Business, DeliveryJob, Driver, Order
from ed_domain.core.entities.delivery_job import (WayPoint, WaypointStatus,
                                                  WayPointType)
from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.entities.order import OrderStatus
from ed_domain.core.entities.otp import OtpVerificationAction
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.utils.otp.abc_otp_generator import ABCOtpGenerator
from ed_notification.documentation.endpoints import NotificationDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_core.application.features.driver.dtos import PickUpOrderDto
from ed_core.application.features.driver.requests.commands import \
    PickUpOrderCommand
from ed_core.common.generic_helpers import get_new_id


@request_handler(PickUpOrderCommand, BaseResponse[PickUpOrderDto])
class PickUpOrderCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, api: ABCApi, otp: ABCOtpGenerator):
        self._uow = uow
        self._api = api
        self._otp = otp

    async def handle(self, request: PickUpOrderCommand) -> BaseResponse[PickUpOrderDto]:
        delivery_job = self._validate_delivery_job(request.delivery_job_id)
        driver = self._validate_driver(request.driver_id, delivery_job)
        order = self._validate_order(request.order_id)

        waypoint_index = self._get_order_waypoint(
            order["id"], delivery_job["waypoints"]
        )

        # Send otp to business
        business = self._validate_business(order["business_id"])
        sms_otp = self._otp.generate()
        self._send_notification(
            business["id"],
            f"Your OTP for delivery job {delivery_job['id']} is {sms_otp}.",
        )

        # Update db
        order["order_status"] = OrderStatus.IN_PROGRESS
        delivery_job["waypoints"][waypoint_index][
            "waypoint_status"
        ] = WaypointStatus.IN_PROGRESS

        self._uow.delivery_job_repository.update(delivery_job["id"], delivery_job)
        self._uow.otp_repository.create(
            {
                "id": get_new_id(),
                "user_id": driver["user_id"],
                "value": sms_otp,
                "action": OtpVerificationAction.PICK_UP,
                "expiry_datetime": datetime.now(UTC) + timedelta(minutes=5),
                "create_datetime": datetime.now(UTC),
                "update_datetime": datetime.now(UTC),
                "deleted": False,
            }
        )
        self._uow.order_repository.update(order["id"], order)
        self._uow.driver_repository.update(driver["id"], driver)

        return BaseResponse[PickUpOrderDto].success(
            "Delivery job verification OTP sent to business.",
            PickUpOrderDto(
                order_id=order["id"], driver_id=driver["id"], business_id=business["id"]
            ),
        )

    def _send_notification(self, user_id: UUID, message: str) -> NotificationDto:
        notification_response = self._api.notification_api.send_notification(
            {
                "user_id": user_id,
                "notification_type": NotificationType.SMS,
                "message": message,
            }
        )

        if not notification_response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Delivery job not picked up.",
                [
                    f"Failed to send notification to business with id {user_id}.",
                    notification_response["message"],
                ],
            )

        return notification_response["data"]

    def _get_order_waypoint(self, order_id: UUID, waypoints: list[WayPoint]) -> int:
        for index, waypoint in enumerate(waypoints):
            if (
                waypoint["order_id"] == order_id
                and waypoint["type"] == WayPointType.PICK_UP
            ):
                return index

        raise ApplicationException(
            Exceptions.BadRequestException,
            "Order not found in waypoints.",
            [f"Order with id {order_id} is not in the delivery job waypoints."],
        )

    def _validate_delivery_job(self, delivery_job_id: UUID) -> DeliveryJob:
        delivery_job = self._uow.delivery_job_repository.get(id=delivery_job_id)
        if not delivery_job or "driver_id" not in delivery_job:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Delivery job not found.",
                [f"Delivery job with id {delivery_job_id} not found."],
            )
        return delivery_job

    def _validate_driver(self, driver_id: UUID, delivery_job: DeliveryJob) -> Driver:
        driver = self._uow.driver_repository.get(id=driver_id)
        if not driver:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Driver not found.",
                [f"Driver with id {driver_id} not found."],
            )

        if driver["id"] != delivery_job.get("driver_id"):
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Driver mismatch.",
                [
                    "Driver ID is different from the one registered for the delivery job."
                ],
            )
        return driver

    def _validate_order(self, order_id: UUID) -> Order:
        order = self._uow.order_repository.get(id=order_id)
        if not order:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Order not found.",
                [f"Order with id {order_id} not found."],
            )
        return order

    def _validate_business(self, business_id: UUID) -> Business:
        business = self._uow.business_repository.get(id=business_id)
        if not business:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Delivery job not picked up.",
                [f"Business with id {business_id} not found."],
            )

        return business
