from abc import ABCMeta

from ed_domain.core.entities.delivery_job import DeliveryJob
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCDeliveryJobRepository(
    ABCGenericRepository[DeliveryJob],
    metaclass=ABCMeta,
):
    ...
