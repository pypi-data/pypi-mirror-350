from datetime import UTC, datetime

from ed_domain.core.entities import Business, Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.dtos import CreateLocationDto
from ed_core.application.features.business.dtos.validators import \
    CreateBusinessDtoValidator
from ed_core.application.features.business.requests.commands import \
    CreateBusinessCommand
from ed_core.application.features.common.dtos.business_dto import BusinessDto
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateBusinessCommand, BaseResponse[BusinessDto])
class CreateBusinessCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateBusinessCommand) -> BaseResponse[BusinessDto]:
        dto_validator = CreateBusinessDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[BusinessDto].error(
                "Create business failed.", dto_validator.errors
            )

        dto = request.dto
        location = await self._create_location(dto["location"])

        business = self._uow.business_repository.create(
            Business(
                id=get_new_id(),
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
                user_id=dto["user_id"],
                notification_ids=[],
                active_status=True,
                business_name=dto["business_name"],
                owner_first_name=dto["owner_first_name"],
                owner_last_name=dto["owner_last_name"],
                phone_number=dto["phone_number"],
                email=dto["email"],
                location_id=location["id"],
                billing_details=[],
                bills=[],
            )
        )

        return BaseResponse[BusinessDto].success(
            "Business created successfully.",
            BusinessDto.from_business(business, self._uow),
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
