from abc import ABCMeta, abstractmethod

from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription


class ABCQueueDescriptions(metaclass=ABCMeta):
    @property
    @abstractmethod
    def descriptions(self) -> list[QueueDescription]: ...

    def get_queue(self, name: str) -> QueueDescription:
        for description in self.descriptions:
            if description["name"] == name:
                return description

        raise ValueError(f"Queue description not found for {name}")
