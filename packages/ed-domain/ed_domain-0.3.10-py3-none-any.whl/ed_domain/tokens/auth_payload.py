from enum import StrEnum
from typing import TypedDict


class UserType(StrEnum):
    ADMIN = "admin"
    CONSUMER = "consumer"
    BUSINESS = "business"
    DRIVER = "driver"


class AuthPayload(TypedDict):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    user_type: UserType
