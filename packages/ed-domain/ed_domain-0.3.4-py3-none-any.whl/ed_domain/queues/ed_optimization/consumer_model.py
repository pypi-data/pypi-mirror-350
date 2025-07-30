from typing import TypedDict
from uuid import UUID

from ed_domain.queues.ed_optimization.location_model import LocationModel


class ConsumerModel(TypedDict):
    id: UUID
    location: LocationModel
