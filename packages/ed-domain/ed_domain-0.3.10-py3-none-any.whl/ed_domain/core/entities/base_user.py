from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity


class BaseUser(BaseEntity):
    user_id: UUID
    active_status: bool
