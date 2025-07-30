from datetime import datetime
from typing import TypedDict
from uuid import UUID


class BaseEntity(TypedDict):
    id: UUID
    create_datetime: datetime
    update_datetime: datetime
    deleted: bool
