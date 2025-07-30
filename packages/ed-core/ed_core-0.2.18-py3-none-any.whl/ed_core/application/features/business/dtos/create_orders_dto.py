from datetime import datetime
from typing import TypedDict

from ed_domain.core.entities.order import Parcel

from ed_core.application.features.business.dtos.create_location_dto import \
    CreateLocationDto


class CreateConsumerDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto


class CreateOrderDto(TypedDict):
    consumer: CreateConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel


class CreateOrdersDto(TypedDict):
    orders: list[CreateOrderDto]
