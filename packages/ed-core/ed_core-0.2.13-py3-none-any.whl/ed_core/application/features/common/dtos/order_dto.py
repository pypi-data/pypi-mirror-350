from datetime import datetime
from typing import Optional
from uuid import UUID

from ed_domain.core.entities.order import Order, OrderStatus, Parcel
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos import BusinessDto, ConsumerDto
from ed_core.application.features.common.dtos.bill_dto import BillDto


class OrderDto(BaseModel):
    id: UUID
    business: BusinessDto
    consumer: ConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: OrderStatus
    delivery_job_id: Optional[UUID]
    bill: BillDto

    @classmethod
    def from_order(
        cls,
        order: Order,
        uow: ABCUnitOfWork,
    ) -> "OrderDto":
        order_consumer = uow.consumer_repository.get(id=order["consumer_id"])
        assert (
            order_consumer is not None
        ), f"Consumer with id: {order['consumer_id']} not found"

        order_business = uow.business_repository.get(id=order["business_id"])
        assert order_business is not None, "Business not found"

        bill = uow.bill_repository.get(id=order["bill_id"])
        assert bill is not None, "Bill not found"

        return cls(
            id=order["id"],
            business=BusinessDto.from_business(order_business, uow),
            consumer=ConsumerDto.from_consumer(order_consumer, uow),
            latest_time_of_delivery=order["latest_time_of_delivery"],
            parcel=order["parcel"],
            order_status=order["order_status"],
            delivery_job_id=order.get("delivery_job_id"),
            bill=BillDto.from_bill(bill),
        )
