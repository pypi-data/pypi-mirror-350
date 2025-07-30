from functools import wraps
from typing import Awaitable, Callable, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

from ed_core.application.common.responses.base_response import BaseResponse

T = TypeVar("T")


class _ApiResponse(BaseModel):
    is_success: bool = Field(...)
    message: str = Field(...)


class GenericResponse(_ApiResponse, Generic[T]):
    data: Optional[T] = None
    errors: list[str] = []

    @staticmethod
    def from_response(base_response: BaseResponse[T]) -> "GenericResponse[T]":
        return GenericResponse[T](
            is_success=base_response.is_success,
            message=base_response.message,
            data=base_response.data,
            errors=base_response.errors,
        )

    def to_dict(self) -> dict:
        return {
            "is_success": self.is_success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors,
        }


def rest_endpoint(
    func: Callable[..., Awaitable[BaseResponse]],
) -> Callable[..., Awaitable[GenericResponse]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> GenericResponse:
        response = await func(*args, **kwargs)
        return GenericResponse.from_response(response)

    return wrapper
