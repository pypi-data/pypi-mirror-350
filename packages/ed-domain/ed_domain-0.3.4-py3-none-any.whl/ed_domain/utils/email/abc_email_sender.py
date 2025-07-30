from abc import ABCMeta, abstractmethod


class ABCEmailSender(metaclass=ABCMeta):
    @abstractmethod
    async def send(
        self, sender: str, recipient: str, subject: str, html: str
    ) -> None: ...
