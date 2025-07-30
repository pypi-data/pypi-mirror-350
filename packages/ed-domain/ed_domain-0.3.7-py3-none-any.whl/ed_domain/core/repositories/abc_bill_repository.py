from abc import ABCMeta

from ed_domain.core.entities.bill import Bill
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCBillRepository(
    ABCGenericRepository[Bill],
    metaclass=ABCMeta,
):
    ...
