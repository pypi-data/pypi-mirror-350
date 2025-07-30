from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities.order import OrderStatus
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import OrderDto
from ed_core.application.features.order.requests.commands import \
    CancelOrderCommand


@request_handler(CancelOrderCommand, BaseResponse[OrderDto])
class CancelOrderCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CancelOrderCommand) -> BaseResponse[OrderDto]:
        if order := self._uow.order_repository.get(id=request.order_id):
            order["order_status"] = OrderStatus.CANCELLED
            order["update_datetime"] = datetime.now(UTC)

            if self._uow.order_repository.update(order["id"], order):
                return BaseResponse[OrderDto].success(
                    "Order cancelled successfully.",
                    OrderDto.from_order(order, self._uow),
                )

            # TODO: Let optimization know about order cancelling

            raise ApplicationException(
                Exceptions.InternalServerException,
                "Cancel order failed.",
                [f"Internal error while cancelling order with id {request.order_id}."],
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Cancel order failed.",
            [f"Order with id {request.order_id} not found."],
        )
