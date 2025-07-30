from abc import ABCMeta, abstractmethod
from typing import Generic, List, TypeVar


class ValidationResponse:
    def __init__(self, is_valid: bool, errors: List[str] = []):
        self.is_valid = is_valid
        self.errors = errors

    @staticmethod
    def valid() -> "ValidationResponse":
        return ValidationResponse(is_valid=True)

    @staticmethod
    def invalid(errors: List[str]) -> "ValidationResponse":
        return ValidationResponse(is_valid=False, errors=errors)


TDto = TypeVar("TDto")


class ABCDtoValidator(Generic[TDto], metaclass=ABCMeta):
    @abstractmethod
    def validate(self, dto: TDto) -> ValidationResponse:
        pass
