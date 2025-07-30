from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

Payload = TypeVar("Payload")


class ABCJwtHandler(Generic[Payload], metaclass=ABCMeta):
    @abstractmethod
    def encode(self, payload: Payload) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> Payload: ...
