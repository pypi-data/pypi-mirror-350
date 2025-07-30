from typing import TypedDict
from uuid import UUID


class LocationModel(TypedDict):
    id: UUID
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str
    country: str
