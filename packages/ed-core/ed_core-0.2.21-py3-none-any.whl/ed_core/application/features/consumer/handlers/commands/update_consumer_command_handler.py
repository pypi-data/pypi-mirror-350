from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Consumer, Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.consumer_dto import ConsumerDto
from ed_core.application.features.consumer.dtos.update_consumer_dto import (
    UpdateConsumerDto, UpdateLocationDto)
from ed_core.application.features.consumer.dtos.validators import \
    UpdateConsumerDtoValidator
from ed_core.application.features.consumer.requests.commands import \
    UpdateConsumerCommand
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateConsumerCommand, BaseResponse[ConsumerDto])
class UpdateConsumerCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: UpdateConsumerCommand) -> BaseResponse[ConsumerDto]:
        dto_validator = UpdateConsumerDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[ConsumerDto].error(
                "Update consumer failed.", dto_validator.errors
            )

        dto = request.dto

        if consumer := self._uow.consumer_repository.get(id=request.consumer_id):
            location = (
                await self._create_location(dto["location"])
                if "location" in dto
                else {"id": consumer["location_id"]}
            )
            consumer["location_id"] = location["id"]
            consumer["update_datetime"] = datetime.now(UTC)

            self._uow.consumer_repository.update(consumer["id"], consumer)

            return BaseResponse[ConsumerDto].success(
                "Consumer updated successfully.",
                ConsumerDto.from_consumer(consumer, self._uow),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Consumer update failed.",
            ["Consumer not found."],
        )

    async def _create_location(self, location: UpdateLocationDto) -> Location:
        return self._uow.location_repository.create(
            Location(
                **location,
                id=get_new_id(),
                city="Addis Ababa",
                country="Ethiopia",
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
            )
        )

    def _get_from_dto_or_consumer(
        self,
        consumer: Consumer,
        update_consumer_dto: UpdateConsumerDto,
        key: str,
    ) -> str:
        return (
            update_consumer_dto[key]
            if key in update_consumer_dto
            else consumer[key] if key in consumer else ""
        )
