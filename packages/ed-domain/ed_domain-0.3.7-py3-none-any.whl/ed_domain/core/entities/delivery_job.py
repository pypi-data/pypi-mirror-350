from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity
from ed_domain.core.value_objects.money import Money


class WaypointStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class WayPointType(StrEnum):
    PICK_UP = "pick_up"
    DROP_OFF = "drop_off"


class WayPoint(TypedDict):
    order_id: UUID
    eta: datetime
    sequence: int
    type: WayPointType
    waypoint_status: WaypointStatus


class DeliveryJobStatus(StrEnum):
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class DeliveryJob(BaseEntity):
    waypoints: list[WayPoint]
    estimated_payment: Money
    estimated_completion_time: datetime
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
    status: DeliveryJobStatus
    driver_id: NotRequired[UUID]
