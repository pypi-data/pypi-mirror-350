from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DeliveryJobDto
from ed_core.application.features.delivery_job.requests.commands.claim_delivery_job_command import \
    ClaimDeliveryJobCommand


@request_handler(ClaimDeliveryJobCommand, BaseResponse[DeliveryJobDto])
class ClaimDeliveryJobCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: ClaimDeliveryJobCommand
    ) -> BaseResponse[DeliveryJobDto]:
        delivery_job = self._uow.delivery_job_repository.get(id=request.delivery_job_id)
        if not delivery_job:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Delivery job not claimed.",
                [f"Delivery job with id {request.delivery_job_id} not found."],
            )

        driver = self._uow.driver_repository.get(id=request.driver_id)
        if not driver:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Delivery job not claimed.",
                [f"Drier with id {request.driver_id} not found."],
            )

        if "driver_id" in delivery_job and delivery_job["driver_id"] is not None:
            if delivery_job["driver_id"] != request.driver_id:
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Delivery job already claimed.",
                    [
                        f"Delivery job with id {request.delivery_job_id} is already claimed by another driver."
                    ],
                )

            return BaseResponse[DeliveryJobDto].success(
                "Delivery job already claimed by this driver.",
                DeliveryJobDto.from_delivery_job(delivery_job, self._uow),
            )

        delivery_job["driver_id"] = driver["id"]
        self._uow.delivery_job_repository.update(
            request.delivery_job_id,
            delivery_job,
        )

        return BaseResponse[DeliveryJobDto].success(
            "Delivery job Claimed successfully.",
            DeliveryJobDto.from_delivery_job(delivery_job, self._uow),
        )
