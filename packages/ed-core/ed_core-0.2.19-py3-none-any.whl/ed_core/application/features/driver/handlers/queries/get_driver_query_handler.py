from dataclasses import dataclass

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DriverDto
from ed_core.application.features.driver.requests.queries.get_driver_query import \
    GetDriverQuery


@request_handler(GetDriverQuery, BaseResponse[DriverDto])
@dataclass
class GetDriverQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetDriverQuery) -> BaseResponse[DriverDto]:
        if driver := self._uow.driver_repository.get(id=request.driver_id):
            return BaseResponse[DriverDto].success(
                "Driver fetched successfully.",
                DriverDto.from_driver(driver, self._uow),
            )

        return BaseResponse[DriverDto].error(
            "Driver couldn't be fetched.",
            [f"Driver with id {request.driver_id} does not exist."],
        )
