from typing import NotRequired, TypedDict


class UpdateCarDto(TypedDict):
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str


class UpdateLocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str


class UpdateDriverDto(TypedDict):
    profile_image: NotRequired[str]
    phone_number: NotRequired[str]
    email: NotRequired[str]
    location: NotRequired[UpdateLocationDto]
