from ed_domain.core.value_objects.money import Money
from pydantic import BaseModel

from ed_core.application.features.common.dtos.order_dto import OrderDto


class DriverPaymentSummaryDto(BaseModel):
    total_revenue: Money
    debt: Money
    net_revenue: Money
    orders: list[OrderDto]
