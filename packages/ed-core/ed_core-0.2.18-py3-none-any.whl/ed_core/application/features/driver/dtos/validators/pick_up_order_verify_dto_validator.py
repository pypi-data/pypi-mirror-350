from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.pick_up_order_verify_dto import \
    PickUpOrderVerifyDto


class PickUpOrderVerifyDtoValidator(ABCDtoValidator[PickUpOrderVerifyDto]):
    def validate(self, dto: PickUpOrderVerifyDto) -> ValidationResponse:
        errors = []

        # Validate OTP field
        if not dto.get("otp"):
            errors.append("OTP is required")
        elif not dto["otp"].isdigit():
            errors.append("OTP must contain only digits")
        elif len(dto["otp"]) != 6:  # Assuming 6-digit OTP
            errors.append("OTP must be 6 digits")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
