from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_core.application.features.common.dtos.consumer_dto import ConsumerDto
from ed_core.application.features.common.dtos.order_dto import OrderDto
from ed_core.application.features.consumer.dtos import (CreateConsumerDto,
                                                        UpdateConsumerDto)
from ed_core.application.features.consumer.requests.commands import (
    CreateConsumerCommand, UpdateConsumerCommand)
from ed_core.application.features.consumer.requests.queries import (
    GetConsumerByUserIdQuery, GetConsumerOrdersQuery, GetConsumerQuery,
    GetConsumersQuery)
from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/consumers", tags=["Consumer Feature"])


@router.get("", response_model=GenericResponse[list[ConsumerDto]])
@rest_endpoint
async def get_all_consumers(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetConsumersQuery())


@router.post("", response_model=GenericResponse[ConsumerDto])
@rest_endpoint
async def create_consumer(
    request_dto: CreateConsumerDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CreateConsumerCommand(dto=request_dto))


@router.get("/{consumer_id}/orders", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def consumer_orders(
    consumer_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetConsumerOrdersQuery(consumer_id=consumer_id))


@router.get("/{consumer_id}", response_model=GenericResponse[ConsumerDto])
@rest_endpoint
async def get_consumer(
    consumer_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetConsumerQuery(consumer_id=consumer_id))


@router.put("/{consumer_id}", response_model=GenericResponse[ConsumerDto])
@rest_endpoint
async def update_consumer(
    consumer_id: UUID,
    dto: UpdateConsumerDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(UpdateConsumerCommand(consumer_id=consumer_id, dto=dto))


@router.get("/users/{user_id}", response_model=GenericResponse[ConsumerDto])
@rest_endpoint
async def get_consumer_by_user_id(
    user_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetConsumerByUserIdQuery(user_id=user_id))
