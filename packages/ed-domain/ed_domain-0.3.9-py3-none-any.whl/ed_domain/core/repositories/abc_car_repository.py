from abc import ABCMeta

from ed_domain.core.entities.car import Car
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCCarRepository(
    ABCGenericRepository[Car],
    metaclass=ABCMeta,
):
    ...
