from enum import StrEnum
from typing import TypedDict


class Currency(StrEnum):
    ETB = "etb"
    USD = "usd"


class Money(TypedDict):
    amount: float
    currency: Currency
