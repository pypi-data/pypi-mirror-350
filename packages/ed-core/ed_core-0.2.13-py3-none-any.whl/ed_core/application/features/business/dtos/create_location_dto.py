from typing import TypedDict


class CreateLocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str
