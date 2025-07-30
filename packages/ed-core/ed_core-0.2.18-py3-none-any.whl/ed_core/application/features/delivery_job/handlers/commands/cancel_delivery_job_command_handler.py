from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities.delivery_job import DeliveryJobStatus
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DeliveryJobDto
from ed_core.application.features.delivery_job.requests.commands import \
    CancelDeliveryJobCommand


@request_handler(CancelDeliveryJobCommand, BaseResponse[DeliveryJobDto])
class CancelDeliveryJobCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: CancelDeliveryJobCommand
    ) -> BaseResponse[DeliveryJobDto]:
        delivery_job = self._uow.delivery_job_repository.get(id=request.delivery_job_id)
        if not delivery_job:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Delivery job cancelling failed..",
                [f"Delivery job with id {request.delivery_job_id} not found."],
            )

        if delivery_job["status"] == DeliveryJobStatus.CANCELLED:
            return BaseResponse[DeliveryJobDto].success(
                "Delivery job has already been canceled.",
                DeliveryJobDto.from_delivery_job(delivery_job, self._uow),
            )

        if delivery_job["status"] != DeliveryJobStatus.IN_PROGRESS:
            return BaseResponse[DeliveryJobDto].success(
                "Delivery job not in progress.",
                DeliveryJobDto.from_delivery_job(delivery_job, self._uow),
            )

        driver = self._uow.driver_repository.get(id=request.driver_id)
        if not driver:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Delivery job cancelling failed.",
                [f"Driver with id {request.driver_id} not found."],
            )

        if driver["id"] != delivery_job.get("driver_id"):
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Delivery cancelling failed.",
                [
                    "Driver ID is different from the one registered for the delivery job."
                ],
            )

        delivery_job["status"] = DeliveryJobStatus.CANCELLED
        self._uow.delivery_job_repository.update(delivery_job["id"], delivery_job)

        return BaseResponse[DeliveryJobDto].success(
            "Delivery job Canceled successfully.",
            DeliveryJobDto.from_delivery_job(delivery_job, self._uow),
        )
