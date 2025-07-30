from uuid import UUID

from ed_domain.core.entities.base_user import BaseUser


class Business(BaseUser):
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location_id: UUID
