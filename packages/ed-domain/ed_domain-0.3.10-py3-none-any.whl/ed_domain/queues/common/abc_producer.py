from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ABCProducer(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def publish(self, message: T) -> None: ...
