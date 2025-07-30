from datetime import datetime
from enum import StrEnum
from typing import TypedDict
from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity


class WayPointType(StrEnum):
    PICKUP = "PICKUP"
    DROP_OFF = "DROP_OFF"


class WayPoint(TypedDict):
    order_id: UUID
    type: WayPointType
    eta: datetime
    sequence: int


class Route(BaseEntity):
    waypoints: list[WayPoint]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
