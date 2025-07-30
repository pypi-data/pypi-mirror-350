from typing import TypedDict
from uuid import UUID

from ed_core.application.features.business.dtos.create_location_dto import \
    CreateLocationDto


class CreateBusinessDto(TypedDict):
    user_id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
