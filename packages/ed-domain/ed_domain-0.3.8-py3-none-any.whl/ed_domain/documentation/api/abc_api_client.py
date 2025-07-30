from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from ed_domain.documentation.api.definitions import (ApiResponse,
                                                     EndpointCallParams)

ResponseType = TypeVar("ResponseType")


class ABCApiClient(Generic[ResponseType], metaclass=ABCMeta):
    @abstractmethod
    def __call__(
        self, call_params: EndpointCallParams
    ) -> ApiResponse[ResponseType]: ...
