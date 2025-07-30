from datetime import datetime
from typing import Optional
from uuid import UUID

from ed_domain.core.entities.delivery_job import (DeliveryJob,
                                                  DeliveryJobStatus, WayPoint,
                                                  WayPointType)
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos.order_dto import OrderDto


class WayPointDto(BaseModel):
    order: OrderDto
    type: WayPointType
    eta: datetime
    sequence: int

    @classmethod
    def from_waypoint(cls, waypoint: WayPoint, uow: ABCUnitOfWork) -> "WayPointDto":
        waypoint_order = uow.order_repository.get(id=waypoint["order_id"])
        assert waypoint_order is not None, "Order not found"
        return cls(
            order=OrderDto.from_order(waypoint_order, uow),
            type=waypoint["type"],
            eta=waypoint["eta"],
            sequence=waypoint["sequence"],
        )


class DeliveryJobDto(BaseModel):
    id: UUID
    waypoints: list[WayPointDto]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
    driver_id: Optional[UUID]
    status: DeliveryJobStatus
    estimated_payment: float
    estimated_completion_time: datetime

    @classmethod
    def from_delivery_job(
        cls,
        delivery_job: DeliveryJob,
        uow: ABCUnitOfWork,
    ) -> "DeliveryJobDto":
        assert delivery_job["waypoints"], "Waypoints cannot be empty"

        return cls(
            id=delivery_job["id"],
            waypoints=[
                WayPointDto.from_waypoint(waypoint, uow)
                for waypoint in delivery_job["waypoints"]
            ],
            estimated_distance_in_kms=delivery_job["estimated_distance_in_kms"],
            estimated_time_in_minutes=delivery_job["estimated_time_in_minutes"],
            driver_id=delivery_job.get("driver_id"),
            status=delivery_job["status"],
            driver_payment=None,
            estimated_payment=delivery_job["estimated_payment"],
            estimated_completion_time=delivery_job["estimated_completion_time"],
        )
