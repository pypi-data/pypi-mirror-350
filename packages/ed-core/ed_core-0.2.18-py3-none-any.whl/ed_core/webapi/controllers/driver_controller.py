from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_core.application.features.common.dtos import DeliveryJobDto, DriverDto
from ed_core.application.features.common.dtos.order_dto import OrderDto
from ed_core.application.features.delivery_job.requests.commands import (
    CancelDeliveryJobCommand, ClaimDeliveryJobCommand)
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
from ed_core.application.features.driver.requests.commands import (
    CreateDriverCommand, DropOffOrderCommand, DropOffOrderVerifyCommand,
    PickUpOrderCommand, PickUpOrderVerifyCommand, UpdateDriverCommand,
    UpdateDriverCurrentLocationCommand)
from ed_core.application.features.driver.requests.queries import (
    GetAllDriversQuery, GetDriverByUserIdQuery, GetDriverDeliveryJobsQuery,
    GetDriverHeldFundsQuery, GetDriverOrdersQuery,
    GetDriverPaymentSummaryQuery, GetDriverQuery)
from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Feature"])


@router.get("", response_model=GenericResponse[list[DriverDto]])
@rest_endpoint
async def get_all_drivers(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetAllDriversQuery())


@router.post("", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def create_driver(
    request_dto: CreateDriverDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CreateDriverCommand(dto=request_dto))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/pick-up",
    response_model=GenericResponse[PickUpOrderDto],
)
@rest_endpoint
async def initiate_order_pick_up(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(PickUpOrderCommand(driver_id, delivery_job_id, order_id))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/pick-up/verify",
    response_model=GenericResponse[None],
)
@rest_endpoint
async def verify_order_pick_up(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    dto: PickUpOrderVerifyDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        PickUpOrderVerifyCommand(driver_id, delivery_job_id, order_id, dto)
    )


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/drop-off",
    response_model=GenericResponse[DropOffOrderDto],
)
@rest_endpoint
async def initiate_order_drop_off(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        DropOffOrderCommand(driver_id, delivery_job_id, order_id)
    )


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/drop-off/verify",
    response_model=GenericResponse[None],
)
@rest_endpoint
async def verify_order_drop_off(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    dto: DropOffOrderVerifyDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        DropOffOrderVerifyCommand(driver_id, delivery_job_id, order_id, dto)
    )


@router.get(
    "/{driver_id}/delivery-jobs", response_model=GenericResponse[list[DeliveryJobDto]]
)
@rest_endpoint
async def driver_delivery_jobs(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverDeliveryJobsQuery(driver_id))


@router.get(
    "/{driver_id}/payment/summary",
    response_model=GenericResponse[DriverPaymentSummaryDto],
)
@rest_endpoint
async def driver_payment_summary(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverPaymentSummaryQuery(driver_id))


@router.get(
    "/{driver_id}/payment/held-funds",
    response_model=GenericResponse[DriverHeldFundsDto],
)
@rest_endpoint
async def driver_held_funds(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverHeldFundsQuery(driver_id))


@router.get("/{driver_id}/orders", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def driver_orders(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverOrdersQuery(driver_id))


@router.get("/{driver_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def get_driver(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverQuery(driver_id))


@router.put("/{driver_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def update_driver(
    driver_id: UUID,
    dto: UpdateDriverDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(UpdateDriverCommand(driver_id, dto))


@router.put("/{driver_id}/current-location", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def update_driver_current_location(
    driver_id: UUID,
    dto: UpdateLocationDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(UpdateDriverCurrentLocationCommand(driver_id, dto))


@router.get("/users/{user_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def get_driver_by_user_id(
    user_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverByUserIdQuery(user_id))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/claim",
    response_model=GenericResponse[DeliveryJobDto],
)
@rest_endpoint
async def claim_delivery_job(
    driver_id: UUID,
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(ClaimDeliveryJobCommand(driver_id, delivery_job_id))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/cancel",
    response_model=GenericResponse[DeliveryJobDto],
)
@rest_endpoint
async def cancel_delivery_job(
    driver_id: UUID,
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CancelDeliveryJobCommand(driver_id, delivery_job_id))
