from uuid import UUID

from ed_domain.core.entities import Business
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos.location_dto import LocationDto


class BusinessDto(BaseModel):
    id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: LocationDto

    @classmethod
    def from_business(cls, business: Business, uow: ABCUnitOfWork) -> "BusinessDto":
        location = uow.location_repository.get(id=business["location_id"])
        assert location is not None, "Location not found"

        return cls(
            id=business["id"],
            business_name=business["business_name"],
            owner_first_name=business["owner_first_name"],
            owner_last_name=business["owner_last_name"],
            phone_number=business["phone_number"],
            email=business["email"],
            location=LocationDto.from_location(location),
        )
