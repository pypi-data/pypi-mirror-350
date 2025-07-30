from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from ed_domain.common.logging import get_logger
from ed_domain.documentation.common.api_response import ApiResponse
from ed_domain.documentation.common.endpoint_call_params import \
    EndpointCallParams

T = TypeVar("T")
LOG = get_logger()


class ABCApiClient(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, call_params: EndpointCallParams) -> ApiResponse[T]: ...
