from datetime import UTC, datetime

from ed_domain.core.entities import Car, Driver, Location
from ed_domain.core.repositories import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.driver_dto import DriverDto
from ed_core.application.features.driver.dtos.create_driver_dto import (
    CreateCarDto, CreateLocationDto)
from ed_core.application.features.driver.dtos.validators import \
    CreateDriverDtoValidator
from ed_core.application.features.driver.requests.commands import \
    CreateDriverCommand
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateDriverCommand, BaseResponse[DriverDto])
class CreateDriverCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateDriverCommand) -> BaseResponse[DriverDto]:
        dto_validator = CreateDriverDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[DriverDto].error(
                "Create driver failed.", dto_validator.errors
            )

        dto = request.dto
        car = await self._create_car(dto["car"])
        location = await self._create_location(dto["location"])
        driver = self._uow.driver_repository.create(
            Driver(
                user_id=dto["user_id"],
                first_name=dto["first_name"],
                last_name=dto["last_name"],
                phone_number=dto["phone_number"],
                email=dto["email"],
                profile_image=dto["profile_image"],
                id=get_new_id(),
                car_id=car["id"],
                location_id=location["id"],
                notification_ids=[],
                delivery_job_ids=[],
                payment_ids=[],
                active_status=True,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
            )
        )

        return BaseResponse[DriverDto].success(
            "Driver created successfully.",
            DriverDto.from_driver(driver, self._uow),
        )

    async def _create_car(self, car: CreateCarDto) -> Car:
        return self._uow.car_repository.create(
            Car(
                **car,  # type: ignore
                id=get_new_id(),
            )
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
