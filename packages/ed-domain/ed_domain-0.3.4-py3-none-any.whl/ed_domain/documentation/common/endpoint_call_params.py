from typing import Any, NotRequired, TypedDict


class EndpointCallParams(TypedDict):
    headers: NotRequired[dict]
    query_params: NotRequired[dict]
    path_params: NotRequired[dict]
    request: NotRequired[Any]
