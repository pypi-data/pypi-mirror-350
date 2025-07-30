from abc import ABCMeta

from ed_domain.core.entities.business import Business
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCBusinessRepository(
    ABCGenericRepository[Business],
    metaclass=ABCMeta,
):
    ...
