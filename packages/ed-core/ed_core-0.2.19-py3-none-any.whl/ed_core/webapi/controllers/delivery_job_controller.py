from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_core.application.features.common.dtos import DeliveryJobDto
from ed_core.application.features.delivery_job.dtos import CreateDeliveryJobDto
from ed_core.application.features.delivery_job.requests.commands import \
    CreateDeliveryJobCommand
from ed_core.application.features.delivery_job.requests.queries import (
    GetDeliveryJobQuery, GetDeliveryJobsQuery)
from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/delivery-jobs", tags=["Delivery Job Feature"])


@router.get("", response_model=GenericResponse[list[DeliveryJobDto]])
@rest_endpoint
async def get_delivery_jobs(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    result = await mediator.send(GetDeliveryJobsQuery())
    return result


@router.get("/{delivery_job_id}", response_model=GenericResponse[DeliveryJobDto])
@rest_endpoint
async def get_delivery_job(
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    result = await mediator.send(GetDeliveryJobQuery(delivery_job_id))
    return result


@router.post("", response_model=GenericResponse[DeliveryJobDto])
@rest_endpoint
async def create_delivery_job(
    dto: CreateDeliveryJobDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CreateDeliveryJobCommand(dto=dto))
