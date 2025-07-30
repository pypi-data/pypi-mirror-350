from abc import ABCMeta, abstractmethod

from ed_domain.documentation.api.definitions.endpoint_description import \
    EndpointDescription


class ABCEndpointDescriptions(metaclass=ABCMeta):
    @property
    @abstractmethod
    def descriptions(self) -> list[EndpointDescription]: ...

    def get_description(self, name: str) -> EndpointDescription:
        for description in self.descriptions:
            if description["name"] == name:
                return description

        raise ValueError(f"Endpoint description not found for {name}")
