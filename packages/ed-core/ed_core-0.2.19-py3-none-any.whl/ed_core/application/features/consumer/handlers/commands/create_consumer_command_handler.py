from datetime import UTC, datetime

from ed_domain.core.entities import Consumer, Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.consumer_dto import ConsumerDto
from ed_core.application.features.consumer.dtos.create_consumer_dto import \
    CreateLocationDto
from ed_core.application.features.consumer.dtos.validators import \
    CreateConsumerDtoValidator
from ed_core.application.features.consumer.requests.commands import \
    CreateConsumerCommand
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateConsumerCommand, BaseResponse[ConsumerDto])
class CreateConsumerCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateConsumerCommand) -> BaseResponse[ConsumerDto]:
        dto_validator = CreateConsumerDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[ConsumerDto].error(
                "Create consumer failed.", dto_validator.errors
            )

        dto = request.dto
        location = await self._create_location(dto["location"])
        consumer = self._uow.consumer_repository.create(
            Consumer(
                user_id=dto["user_id"],
                first_name=dto["first_name"],
                last_name=dto["last_name"],
                phone_number=dto["phone_number"],
                email=dto["email"],
                id=get_new_id(),
                location_id=location["id"],
                notification_ids=[],
                active_status=True,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
            )
        )

        return BaseResponse[ConsumerDto].success(
            "Consumer created successfully.",
            ConsumerDto.from_consumer(consumer, self._uow),
        )

    async def _create_location(self, location: CreateLocationDto) -> Location:
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
