from typing import Optional

from ed_domain.core.entities import DeliveryJob, Driver
from ed_domain.core.entities.order import Order
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos.delivery_job_dto import \
    DeliveryJobDto
from ed_core.application.features.common.dtos.driver_dto import DriverDto
from ed_core.application.features.common.dtos.order_dto import OrderDto


class TrackOrderDto(BaseModel):
    order: OrderDto
    delivery_job: Optional[DeliveryJobDto]
    driver: Optional[DriverDto]

    @classmethod
    def from_entities(
        cls,
        order: Order,
        uow: ABCUnitOfWork,
        delivery_job: Optional[DeliveryJob] = None,
        driver: Optional[Driver] = None,
    ) -> "TrackOrderDto":
        return cls(
            order=OrderDto.from_order(order, uow),
            delivery_job=(
                DeliveryJobDto.from_delivery_job(delivery_job, uow)
                if delivery_job
                else None
            ),
            driver=DriverDto.from_driver(driver, uow) if driver else None,
        )
