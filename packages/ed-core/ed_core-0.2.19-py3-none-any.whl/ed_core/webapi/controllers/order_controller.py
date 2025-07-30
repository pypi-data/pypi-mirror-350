from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_core.application.features.common.dtos import OrderDto
from ed_core.application.features.common.dtos.track_order_dto import \
    TrackOrderDto
from ed_core.application.features.order.requests.commands import \
    CancelOrderCommand
from ed_core.application.features.order.requests.queries import (
    GetOrderQuery, GetOrdersQuery)
from ed_core.application.features.order.requests.queries.track_order_query import \
    TrackOrderQuery
from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/orders", tags=["Order Feature"])


@router.get("", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def get_orders(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info("Satisfying get_orders request")
    return await mediator.send(GetOrdersQuery())


@router.get("/{order_id}", response_model=GenericResponse[OrderDto])
@rest_endpoint
async def get_order(
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info("Satisfying get_order request")
    return await mediator.send(GetOrderQuery(order_id=order_id))


@router.post("/{order_id}/cancel", response_model=GenericResponse[OrderDto])
@rest_endpoint
async def cancel_order(
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    LOG.info("Satisfying cancel_order request")
    return await mediator.send(CancelOrderCommand(order_id=order_id))


@router.get("/{order_id}/track", response_model=GenericResponse[TrackOrderDto])
@rest_endpoint
async def track_order(
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        TrackOrderQuery(
            order_id=order_id,
        )
    )
