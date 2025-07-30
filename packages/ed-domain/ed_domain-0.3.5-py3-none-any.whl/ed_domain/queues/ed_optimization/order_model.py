from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain.core.entities.order import Parcel
from ed_domain.queues.ed_optimization.business_model import BusinessModel
from ed_domain.queues.ed_optimization.consumer_model import ConsumerModel


class OrderModel(TypedDict):
    id: UUID
    consumer: ConsumerModel
    business: BusinessModel
    latest_time_of_delivery: datetime
    parcel: Parcel
    create_datetime: datetime
