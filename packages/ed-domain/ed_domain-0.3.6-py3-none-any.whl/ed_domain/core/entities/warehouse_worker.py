from uuid import UUID

from ed_domain.core.entities.base_user import BaseUser


class WarehouseWorker(BaseUser):
    id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: str
