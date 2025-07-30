from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

RequestModel = TypeVar("RequestModel")


class ABCRabbitProducer(Generic[RequestModel], metaclass=ABCMeta):
    @abstractmethod
    def send(self, request: RequestModel) -> None: ...
