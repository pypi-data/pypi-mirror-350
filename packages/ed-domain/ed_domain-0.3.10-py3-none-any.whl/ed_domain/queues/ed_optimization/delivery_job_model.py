from datetime import timedelta
from typing import Literal, TypedDict
from uuid import UUID

from ed_domain.core.entities.delivery_job import DeliveryJobStatus
from ed_domain.core.value_objects.money import Money


class DeliveryJobModel(TypedDict):
    route_id: UUID
    status: Literal[DeliveryJobStatus.AVAILABLE]
    estimated_payment: Money
    estimated_completion_time: timedelta
