from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from ed_domain.documentation.api.definitions import (ApiResponse,
                                                     EndpointCallParams)

TResponseType = TypeVar("TResponseType")


class ABCEndpointClient(Generic[TResponseType], metaclass=ABCMeta):
    @abstractmethod
    def __call__(
        self, call_params: EndpointCallParams
    ) -> ApiResponse[TResponseType]: ...
