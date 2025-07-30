from typing import NotRequired
from uuid import UUID

from ed_domain.core.entities.base_user import BaseUser


class Driver(BaseUser):
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    location_id: UUID
    car_id: UUID
    current_location_id: UUID
