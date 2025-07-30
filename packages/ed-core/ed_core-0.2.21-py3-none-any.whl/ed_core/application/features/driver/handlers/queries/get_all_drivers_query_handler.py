from dataclasses import dataclass

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DriverDto
from ed_core.application.features.driver.requests.queries.get_all_drivers_query import \
    GetAllDriversQuery


@request_handler(GetAllDriversQuery, BaseResponse[list[DriverDto]])
@dataclass
class GetAllDriversQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetAllDriversQuery
    ) -> BaseResponse[list[DriverDto]]:
        if drivers := self._uow.driver_repository.get_all():
            return BaseResponse[list[DriverDto]].success(
                "Drivers fetched successfully.",
                [DriverDto.from_driver(driver, self._uow) for driver in drivers],
            )

        return BaseResponse[list[DriverDto]].error(
            "Drivers couldn't be fetched.", ["There are no drivers."]
        )
