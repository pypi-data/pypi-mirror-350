from abc import ABCMeta

from ed_domain.core.entities.consumer import Consumer
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCConsumerRepository(
    ABCGenericRepository[Consumer],
    metaclass=ABCMeta,
):
    ...
