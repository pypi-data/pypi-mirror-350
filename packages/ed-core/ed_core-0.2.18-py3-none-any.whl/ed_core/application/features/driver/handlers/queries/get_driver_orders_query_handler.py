from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import OrderDto
from ed_core.application.features.driver.requests.queries import \
    GetDriverOrdersQuery


@request_handler(GetDriverOrdersQuery, BaseResponse[list[OrderDto]])
class GetDriverOrdersQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDriverOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        orders = self._uow.order_repository.get_all(
            driver_id=request.driver_id)
        if not orders:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Driver orders could not fetched.",
                [f"Orders for driver with id {request.driver_id} not found."],
            )

        return BaseResponse[list[OrderDto]].success(
            "Driver orders fetched successfully.",
            [OrderDto.from_order(order, self._uow) for order in orders],
        )
