from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.requests.queries import \
    GetBusinessOrdersQuery
from ed_core.application.features.common.dtos import OrderDto


@request_handler(GetBusinessOrdersQuery, BaseResponse[list[OrderDto]])
class GetBusinessOrdersQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetBusinessOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        return BaseResponse[list[OrderDto]].success(
            "Orders fetched successfully.",
            [
                OrderDto.from_order(order, self._uow)
                for order in self._uow.order_repository.get_all(
                    business_id=request.business_id
                )
            ],
        )
