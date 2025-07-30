from abc import ABCMeta

from ed_domain.core.entities.location import Location
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCLocationRepository(
    ABCGenericRepository[Location],
    metaclass=ABCMeta,
):
    ...
