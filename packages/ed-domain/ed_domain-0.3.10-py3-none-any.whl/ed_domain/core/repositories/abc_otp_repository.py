from abc import ABCMeta

from ed_domain.core.entities.otp import Otp
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCOtpRepository(
    ABCGenericRepository[Otp],
    metaclass=ABCMeta,
):
    ...
