from typing import TypedDict
from uuid import UUID


class CreateCarDto(TypedDict):
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str


class CreateLocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str


class CreateDriverDto(TypedDict):
    user_id: UUID
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: str
    location: CreateLocationDto
    car: CreateCarDto
