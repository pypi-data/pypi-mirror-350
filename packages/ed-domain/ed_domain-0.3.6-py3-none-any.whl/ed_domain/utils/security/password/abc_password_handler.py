from abc import ABCMeta, abstractmethod


class ABCPasswordHandler(metaclass=ABCMeta):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, hash: str) -> bool: ...
