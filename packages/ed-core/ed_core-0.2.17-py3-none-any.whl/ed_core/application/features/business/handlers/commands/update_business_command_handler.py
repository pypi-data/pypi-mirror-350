from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Business, Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.dtos import CreateLocationDto
from ed_core.application.features.business.dtos.update_business_dto import \
    UpdateBusinessDto
from ed_core.application.features.business.dtos.validators import \
    UpdateBusinessDtoValidator
from ed_core.application.features.business.requests.commands import \
    UpdateBusinessCommand
from ed_core.application.features.common.dtos.business_dto import BusinessDto
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateBusinessCommand, BaseResponse[BusinessDto])
class UpdateBusinessCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: UpdateBusinessCommand) -> BaseResponse[BusinessDto]:
        dto_validator = UpdateBusinessDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[BusinessDto].error(
                "Update business failed.", dto_validator.errors
            )

        dto = request.dto

        if business := self._uow.business_repository.get(id=request.id):
            location = (
                await self._create_location(dto["location"])
                if "location" in dto
                else None
            )
            business["phone_number"] = self._get_from_dto_or_business(
                business, dto, "phone_number"
            )
            business["email"] = self._get_from_dto_or_business(business, dto, "email")
            business["location_id"] = (
                location["id"] if location else business["location_id"]
            )
            business["update_datetime"] = datetime.now(UTC)
            business["billing_details"] = (
                dto["billing_details"]
                if "billing_details" in dto
                else business["billing_details"]
            )
            is_business_updated = self._uow.business_repository.update(
                business["id"], business
            )
            if not is_business_updated:
                raise ApplicationException(
                    Exceptions.InternalServerException,
                    "Business update failed.",
                    ["Internal server error."],
                )

            return BaseResponse[BusinessDto].success(
                "Business updated successfully.",
                BusinessDto.from_business(business, self._uow),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Business update failed.",
            ["Business not found."],
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

    def _get_from_dto_or_business(
        self,
        driver: Business,
        update_business_dto: UpdateBusinessDto,
        key: str,
    ) -> str:
        return (
            update_business_dto[key]
            if key in update_business_dto
            else driver[key] if key in driver else ""
        )
