from abc import ABCMeta

from ed_domain.core.entities.order import Order
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCOrderRepository(
    ABCGenericRepository[Order],
    metaclass=ABCMeta,
):
    ...
