from ed_domain.core.entities import Location
from pydantic import BaseModel


class LocationDto(BaseModel):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str

    @classmethod
    def from_location(cls, location: Location) -> "LocationDto":
        return cls(
            address=location["address"],
            latitude=location["latitude"],
            longitude=location["longitude"],
            postal_code=location["postal_code"],
            city=location["city"],
        )
