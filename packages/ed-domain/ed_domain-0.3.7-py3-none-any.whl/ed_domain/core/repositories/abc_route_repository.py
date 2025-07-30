from abc import ABCMeta

from ed_domain.core.entities.route import Route
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCRouteRepository(
    ABCGenericRepository[Route],
    metaclass=ABCMeta,
):
    ...
