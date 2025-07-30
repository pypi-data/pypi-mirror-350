from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Driver, Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.driver_dto import DriverDto
from ed_core.application.features.driver.dtos.update_driver_dto import (
    UpdateDriverDto, UpdateLocationDto)
from ed_core.application.features.driver.dtos.validators import \
    UpdateDriverDtoValidator
from ed_core.application.features.driver.requests.commands import \
    UpdateDriverCommand
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateDriverCommand, BaseResponse[DriverDto])
class UpdateDriverCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: UpdateDriverCommand) -> BaseResponse[DriverDto]:
        dto_validator = UpdateDriverDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[DriverDto].error(
                "Update driver failed.", dto_validator.errors
            )

        dto = request.dto

        if driver := self._uow.driver_repository.get(id=request.driver_id):
            location = (
                await self._create_location(dto["location"])
                if "location" in dto
                else {"id": driver["location_id"]}
            )
            driver["first_name"] = self._get_from_dto_or_driver(
                driver, dto, "first_name"
            )
            driver["last_name"] = self._get_from_dto_or_driver(driver, dto, "last_name")
            driver["phone_number"] = self._get_from_dto_or_driver(
                driver, dto, "phone_number"
            )
            driver["email"] = self._get_from_dto_or_driver(driver, dto, "email")
            driver["profile_image"] = self._get_from_dto_or_driver(
                driver, dto, "profile_image"
            )
            driver["location_id"] = location["id"]
            driver["update_datetime"] = datetime.now(UTC)

            self._uow.driver_repository.update(driver["id"], driver)

            return BaseResponse[DriverDto].success(
                "Driver updated successfully.",
                DriverDto.from_driver(driver, self._uow),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Driver update failed.",
            ["Driver not found."],
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

    def _get_from_dto_or_driver(
        self,
        driver: Driver,
        update_driver_dto: UpdateDriverDto,
        key: str,
    ) -> str:
        return (
            update_driver_dto[key]
            if key in update_driver_dto
            else driver[key] if key in driver else ""
        )
