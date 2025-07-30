from typing import NotRequired, TypedDict


class QueueDescription(TypedDict):
    queue: str
    durable: bool
    request_model: NotRequired[type]
