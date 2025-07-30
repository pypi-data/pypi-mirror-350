from enum import StrEnum
from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity


class NotificationType(StrEnum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    IN_APP = "IN_APP"


class Notification(BaseEntity):
    user_id: UUID
    notification_type: NotificationType
    message: str
    read_status: bool
