from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import OrderDto
from ed_core.application.features.consumer.requests.queries import \
    GetConsumerOrdersQuery


@request_handler(GetConsumerOrdersQuery, BaseResponse[list[OrderDto]])
class GetConsumerOrdersQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetConsumerOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        if orders := self._uow.order_repository.get_all(
            consumer_id=request.consumer_id
        ):
            return BaseResponse[list[OrderDto]].success(
                "Order fetched successfully.",
                [OrderDto.from_order(order, self._uow) for order in orders],
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Orders not found.",
            [f"Orders for consumer with id {request.consumer_id} not found."],
        )
