from typing import Optional
from uuid import UUID

from ed_domain.core.entities.consumer import Consumer
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos import LocationDto


class ConsumerDto(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[str]
    location: LocationDto

    @classmethod
    def from_consumer(cls, consumer: Consumer, uow: ABCUnitOfWork) -> "ConsumerDto":
        location = uow.location_repository.get(id=consumer["location_id"])
        assert location is not None, "Location not found"

        return cls(
            id=consumer["id"],
            first_name=consumer["first_name"],
            last_name=consumer["last_name"],
            phone_number=consumer["phone_number"],
            email=consumer["email"],
            location=LocationDto.from_location(location),
        )
