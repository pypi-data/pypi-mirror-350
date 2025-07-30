from typing import Generic, NotRequired, TypedDict, TypeVar

DataType = TypeVar("DataType")


class ApiResponse(Generic[DataType], TypedDict):
    is_success: bool
    message: str
    data: DataType
    http_status_code: NotRequired[int]
    errors: list[str]
