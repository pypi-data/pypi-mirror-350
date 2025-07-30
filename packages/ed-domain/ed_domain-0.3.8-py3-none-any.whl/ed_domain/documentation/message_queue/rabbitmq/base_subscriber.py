from abc import ABCMeta, abstractmethod

from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription


class BaseRabbitmqSubscriber(metaclass=ABCMeta):
    @property
    @abstractmethod
    def descriptions(self) -> list[QueueDescription]: ...

    def get_queue(self, queue: str) -> QueueDescription:
        for description in self.descriptions:
            if description["queue"] == queue:
                return description

        raise ValueError(f"Queue description not found for {queue}")
