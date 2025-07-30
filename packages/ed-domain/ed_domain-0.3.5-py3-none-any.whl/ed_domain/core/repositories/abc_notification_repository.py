from abc import ABCMeta

from ed_domain.core.entities.notification import Notification
from ed_domain.core.repositories.abc_generic_repository import \
    ABCGenericRepository


class ABCNotificationRepository(
    ABCGenericRepository[Notification],
    metaclass=ABCMeta,
):
    ...
