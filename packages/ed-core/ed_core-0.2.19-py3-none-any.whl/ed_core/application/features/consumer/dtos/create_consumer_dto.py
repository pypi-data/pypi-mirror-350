from typing import TypedDict
from uuid import UUID

from ed_core.application.features.driver.dtos.create_driver_dto import \
    CreateLocationDto


class CreateConsumerDto(TypedDict):
    user_id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
