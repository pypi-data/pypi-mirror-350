from datetime import datetime
from enum import StrEnum
from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity


class OtpVerificationAction(StrEnum):
    VERIFY_EMAIL = "VERIFY_EMAIL"
    VERIFY_PHONE_NUMBER = "VERIFY_PHONE_NUMBER"
    LOGIN = "LOGIN"
    PICK_UP = "PICK_UP"
    DROP_OFF = "DROP_OFF"


class Otp(BaseEntity):
    user_id: UUID
    value: str
    action: OtpVerificationAction
    expiry_datetime: datetime
