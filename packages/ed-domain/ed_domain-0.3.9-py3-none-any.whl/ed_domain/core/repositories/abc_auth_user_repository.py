from abc import ABCMeta

from ed_domain.core.entities.auth_user import AuthUser
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCAuthUserRepository(
    ABCGenericRepository[AuthUser],
    metaclass=ABCMeta,
):
    ...
