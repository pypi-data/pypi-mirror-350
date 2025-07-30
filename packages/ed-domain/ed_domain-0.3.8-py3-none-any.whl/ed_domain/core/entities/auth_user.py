from typing import NotRequired

from ed_domain.core.entities.base_entity import BaseEntity


class AuthUser(BaseEntity):
    first_name: str
    last_name: str
    email: NotRequired[str]
    phone_number: NotRequired[str]
    password_hash: str
    verified: bool
    logged_in: bool
