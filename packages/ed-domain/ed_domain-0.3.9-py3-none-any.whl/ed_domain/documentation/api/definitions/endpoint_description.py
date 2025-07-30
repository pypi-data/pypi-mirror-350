from typing import NotRequired, TypedDict

from ed_domain.documentation.api.definitions.http_method import HttpMethod


class EndpointDescription(TypedDict):
    name: str
    path: str
    method: HttpMethod
    headers: NotRequired[type]
    query_params: NotRequired[type]
    path_params: NotRequired[dict[str, type]]
    request_model: NotRequired[type]
    response_model: NotRequired[type]
