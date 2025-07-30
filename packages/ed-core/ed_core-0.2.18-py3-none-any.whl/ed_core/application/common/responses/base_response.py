from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


class BaseResponse(Generic[T]):
    def __init__(
        self, is_success: bool, message: str, data: Optional[T], errors: list[str]
    ):
        self.is_success = is_success
        self.message = message
        self.data = data
        self.errors = errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_success": self.is_success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors,
        }

    @classmethod
    def success(cls, message: str, data: Optional[T] = None) -> "BaseResponse[T]":
        return cls(is_success=True, message=message, data=data, errors=[])

    @classmethod
    def error(cls, message: str, errors: list[str] = []) -> "BaseResponse[T]":
        return cls(is_success=False, message=message, data=None, errors=errors)
