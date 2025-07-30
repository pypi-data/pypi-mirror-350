from ed_domain.core.entities import Car
from pydantic import BaseModel


class CarDto(BaseModel):
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str

    @classmethod
    def from_car(cls, car: Car) -> "CarDto":
        return cls(
            make=car["make"],
            model=car["model"],
            year=car["year"],
            color=car["color"],
            seats=car["seats"],
            license_plate=car["license_plate_number"],
            registration_number=car["registration_number"],
        )
