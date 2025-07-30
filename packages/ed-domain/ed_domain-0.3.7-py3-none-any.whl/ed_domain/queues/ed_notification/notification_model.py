from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain.core.entities.notification import NotificationType


class NotificationModel(TypedDict):
    user_id: UUID
    notification_type: NotificationType
    message: str
    created_datetime: datetime
