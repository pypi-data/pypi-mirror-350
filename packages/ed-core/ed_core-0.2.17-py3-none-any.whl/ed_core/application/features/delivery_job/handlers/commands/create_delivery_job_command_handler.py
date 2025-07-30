from datetime import UTC, datetime

from ed_domain.core.entities import DeliveryJob
from ed_domain.core.entities.delivery_job import DeliveryJobStatus
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DeliveryJobDto
from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto
from ed_core.application.features.delivery_job.requests.commands.create_delivery_job_command import \
    CreateDeliveryJobCommand
from ed_core.common.generic_helpers import get_new_id


@request_handler(CreateDeliveryJobCommand, BaseResponse[DeliveryJobDto])
class CreateDeliveryJobCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: CreateDeliveryJobCommand
    ) -> BaseResponse[DeliveryJobDto]:
        dto: CreateDeliveryJobDto = request.dto

        delivery_job = self._uow.delivery_job_repository.create(
            DeliveryJob(
                id=get_new_id(),
                waypoints=dto["waypoints"],
                estimated_distance_in_kms=dto["estimated_distance_in_kms"],
                estimated_time_in_minutes=dto["estimated_time_in_minutes"],
                status=DeliveryJobStatus.IN_PROGRESS,
                estimated_payment=dto["estimated_payment"],
                estimated_completion_time=dto["estimated_completion_time"],
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
            )
        )

        return BaseResponse[DeliveryJobDto].success(
            "Delivery job created successfully.",
            DeliveryJobDto.from_delivery_job(delivery_job, self._uow),
        )
