from typing import NotRequired, TypedDict


class ConnectionParameters(TypedDict):
    url: str
    queue: str


class QueueDescription(TypedDict):
    name: str
    connection_parameters: ConnectionParameters
    durable: bool
    request_model: NotRequired[type]
