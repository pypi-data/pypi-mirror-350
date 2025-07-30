from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity


class OrderStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ParcelSize(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class ParcelDimensions(TypedDict):
    length: int
    width: int
    height: float


class Parcel(TypedDict):
    size: ParcelSize
    weight: float
    dimensions: ParcelDimensions
    fragile: bool


class Order(BaseEntity):
    consumer_id: UUID
    business_id: UUID
    bill_id: UUID
    driver_id: NotRequired[UUID]
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: OrderStatus
