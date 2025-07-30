from datetime import datetime
from typing import TypedDict

from ed_domain.core.entities.delivery_job import WayPoint


class CreateDeliveryJobDto(TypedDict):
    waypoints: list[WayPoint]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
    estimated_payment: float
    estimated_completion_time: datetime
