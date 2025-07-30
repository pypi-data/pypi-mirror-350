from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

Code = TypeVar("Code")


class ABCOtpGenerator(Generic[Code], metaclass=ABCMeta):
    @abstractmethod
    def generate(self) -> Code: ...
