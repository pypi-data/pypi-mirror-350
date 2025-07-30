from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import OrderDto
from ed_core.application.features.order.requests.queries import GetOrderQuery


@request_handler(GetOrderQuery, BaseResponse[OrderDto])
class GetOrderQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetOrderQuery) -> BaseResponse[OrderDto]:
        if order := self._uow.order_repository.get(id=request.order_id):
            return BaseResponse[OrderDto].success(
                "Order fetched successfully.",
                OrderDto.from_order(order, self._uow),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Order not found.",
            [f"Order with id {request.order_id} not found."],
        )
