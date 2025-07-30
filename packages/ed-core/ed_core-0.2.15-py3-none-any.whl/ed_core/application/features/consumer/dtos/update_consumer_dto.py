from typing import NotRequired, TypedDict


class UpdateLocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str


class UpdateConsumerDto(TypedDict):
    location: NotRequired[UpdateLocationDto]
