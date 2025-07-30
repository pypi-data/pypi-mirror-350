from datetime import datetime

from ed_domain.core.value_objects.money import Money
from pydantic import BaseModel

from ed_core.application.features.common.dtos.order_dto import OrderDto


class DriverHeldFundsDto(BaseModel):
    total_amount: Money
    orders: list[OrderDto]
    due_date: datetime
