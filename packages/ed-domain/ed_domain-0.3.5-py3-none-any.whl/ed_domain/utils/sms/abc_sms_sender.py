from abc import ABCMeta, abstractmethod


class ABCSmsSender(metaclass=ABCMeta):
    @abstractmethod
    async def send(self, recipient: str, message: str) -> None: ...
