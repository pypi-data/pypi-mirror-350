from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Order
from ed_domain.core.entities.bill import BillStatus, Money
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.core.value_objects.money import Currency
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.order_dto import OrderDto
from ed_core.application.features.driver.dtos import DriverPaymentSummaryDto
from ed_core.application.features.driver.requests.queries import \
    GetDriverPaymentSummaryQuery


@request_handler(GetDriverPaymentSummaryQuery, BaseResponse[DriverPaymentSummaryDto])
class GetDriverPaymentSummaryQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDriverPaymentSummaryQuery
    ) -> BaseResponse[DriverPaymentSummaryDto]:
        orders = self._uow.order_repository.get_all(
            driver_id=request.driver_id)
        total, debt = self._get_total_and_outstanding_payment_sum(orders)

        return BaseResponse[DriverPaymentSummaryDto].success(
            "Driver payment summary fetched successfully.",
            DriverPaymentSummaryDto(
                total_revenue=Money(amount=total, currency=Currency.ETB),
                debt=Money(amount=debt, currency=Currency.ETB),
                net_revenue=Money(amount=total - debt, currency=Currency.ETB),
                orders=[OrderDto.from_order(order, self._uow)
                        for order in orders],
            ),
        )

    def _get_total_and_outstanding_payment_sum(
        self, orders: list[Order]
    ) -> tuple[float, float]:
        total_sum: float = 0
        outstanding_sum: float = 0

        for order in orders:
            bill = self._uow.bill_repository.get(id=order["bill_id"])
            if bill is None:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    "Driver payment summary cannot be fetched.",
                    [
                        f"Bill could not be retrieved for the order with id: {order['id']}"
                    ],
                )

            total_sum += bill["amount"]["amount"]
            if bill["bill_status"] == BillStatus.WITH_DRIVER:
                outstanding_sum += bill["amount"]["amount"]

        return total_sum, outstanding_sum
