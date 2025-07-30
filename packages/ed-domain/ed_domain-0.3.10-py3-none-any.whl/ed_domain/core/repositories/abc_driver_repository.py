from abc import ABCMeta

from ed_domain.core.entities.driver import Driver
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCDriverRepository(
    ABCGenericRepository[Driver],
    metaclass=ABCMeta,
):
    ...
