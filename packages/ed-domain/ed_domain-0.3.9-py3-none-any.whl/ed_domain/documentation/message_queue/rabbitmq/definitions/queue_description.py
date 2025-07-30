from typing import NotRequired, TypedDict


class QueueDescription(TypedDict):
    connection_url: str
    name: str
    durable: bool
    request_model: NotRequired[type]
