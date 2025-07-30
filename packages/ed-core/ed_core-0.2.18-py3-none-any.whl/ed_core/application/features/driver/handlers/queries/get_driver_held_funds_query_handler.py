from datetime import UTC, datetime
from uuid import UUID

from ed_domain.core.entities.bill import BillStatus, Money
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.core.value_objects.money import Currency
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.order_dto import OrderDto
from ed_core.application.features.driver.dtos import DriverHeldFundsDto
from ed_core.application.features.driver.requests.queries import \
    GetDriverHeldFundsQuery


@request_handler(GetDriverHeldFundsQuery, BaseResponse[DriverHeldFundsDto])
class GetDriverHeldFundsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDriverHeldFundsQuery
    ) -> BaseResponse[DriverHeldFundsDto]:
        orders = self._get_outstanding_orders(request.driver_id)
        earliest_due_date = datetime.now(UTC)

        if orders:
            valid_due_dates = [
                order.bill.due_date
                for order in orders
                if order.bill.due_date is not None
            ]
            if valid_due_dates:
                earliest_due_date = min(valid_due_dates)

        return BaseResponse[DriverHeldFundsDto].success(
            "Driver orders fetched successfully.",
            DriverHeldFundsDto(
                total_amount=Money(
                    amount=sum(order.bill.amount["amount"]
                               for order in orders),
                    currency=Currency.ETB,
                ),
                orders=orders,
                due_date=earliest_due_date,
            ),
        )

    def _get_outstanding_orders(self, driver_id: UUID) -> list[OrderDto]:
        orders = [
            order
            for order in self._uow.order_repository.get_all(driver_id=driver_id)
            if self._uow.bill_repository.get(
                id=order["bill_id"], bill_status=BillStatus.WITH_DRIVER
            )
        ]

        return [OrderDto.from_order(order, self._uow) for order in orders]
