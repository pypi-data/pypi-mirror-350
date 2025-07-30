from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.driver_dto import DriverDto
from ed_core.application.features.driver.dtos.update_driver_dto import \
    UpdateLocationDto
from ed_core.application.features.driver.dtos.validators.update_driver_dto_validator import \
    UpdateLocationDtoValidator
from ed_core.application.features.driver.requests.commands import \
    UpdateDriverCurrentLocationCommand
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateDriverCurrentLocationCommand, BaseResponse[DriverDto])
class UpdateDriverCurrentLocationCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: UpdateDriverCurrentLocationCommand
    ) -> BaseResponse[DriverDto]:
        dto_validator = UpdateLocationDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[DriverDto].error(
                "Update driver current location failed.", dto_validator.errors
            )

        dto = request.dto

        if driver := self._uow.driver_repository.get(id=request.driver_id):
            location = (
                await self._create_location(dto["location"])
                if "location" in dto
                else {"id": driver["location_id"]}
            )
            driver["current_location_id"] = location["id"]
            self._uow.driver_repository.update(driver["id"], driver)

            return BaseResponse[DriverDto].success(
                "Driver current location updated successfully.",
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
                id=get_new_id(),
                address=location["address"],
                latitude=location["latitude"],
                longitude=location["longitude"],
                postal_code=location["postal_code"],
                city="Addis Ababa",
                country="Ethiopia",
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
                last_used=datetime.now(UTC),
            )
        )
