from datetime import UTC, datetime
from uuid import UUID

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Bill, DeliveryJob, Driver, Order
from ed_domain.core.entities.delivery_job import (WayPoint, WaypointStatus,
                                                  WayPointType)
from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.entities.otp import OtpVerificationAction
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_core.application.features.driver.requests.commands import \
    PickUpOrderVerifyCommand


@request_handler(PickUpOrderVerifyCommand, BaseResponse[None])
class PickUpOrderVerifyCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, api: ABCApi):
        self._uow = uow
        self._api = api

    async def handle(self, request: PickUpOrderVerifyCommand) -> BaseResponse[None]:
        # Get entities
        delivery_job = self._validate_delivery_job(request.delivery_job_id)
        driver = self._validate_driver(request.driver_id, delivery_job)
        order = self._validate_order(request.order_id)
        bill = self._validate_bill(order["bill_id"])

        # Validate otp
        self._validate_otp(driver["user_id"], request.dto["otp"])

        # Update db
        waypoint_index = self._get_order_waypoint(
            order["id"], delivery_job["waypoints"]
        )
        delivery_job["waypoints"][waypoint_index][
            "waypoint_status"
        ] = WaypointStatus.DONE
        self._uow.delivery_job_repository.update(
            delivery_job["id"], delivery_job)

        bill["driver_id"] = driver["id"]
        self._uow.bill_repository.update(bill["id"], bill)

        # Send notifications
        self._api.notification_api.send_notification(
            {
                "user_id": order["business_id"],
                "notification_type": NotificationType.IN_APP,
                "message": f"Order {order['id']} has been picked up by driver {driver['id']}.",
            }
        )

        return BaseResponse[None].success(
            "Delivery job picked up successfully.",
            None,
        )

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
        delivery_job = self._uow.delivery_job_repository.get(
            id=delivery_job_id)
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

    def _validate_otp(self, user_id: UUID, otp_value: str) -> None:
        otp = self._uow.otp_repository.get(user_id=user_id)
        if not otp or otp["action"] != OtpVerificationAction.PICK_UP:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Invalid OTP.",
                ["OTP is not valid or has expired. Please request a new OTP."],
            )

        if otp["expiry_datetime"] < datetime.now(UTC):
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Expired OTP.",
                ["OTP has expired. Please request a new OTP."],
            )

        if otp["value"] != otp_value:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Invalid OTP.",
                ["OTP is not valid. Please request a new OTP."],
            )

    def _validate_order(self, order_id: UUID) -> Order:
        order = self._uow.order_repository.get(id=order_id)
        if not order:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Order not found.",
                [f"Order with id {order_id} not found."],
            )
        return order

    def _validate_bill(self, bill_id: UUID) -> Bill:
        bill = self._uow.bill_repository.get(id=bill_id)
        if not bill:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Bill not found.",
                [f"Bill with id {bill_id} not found."],
            )

        return bill
