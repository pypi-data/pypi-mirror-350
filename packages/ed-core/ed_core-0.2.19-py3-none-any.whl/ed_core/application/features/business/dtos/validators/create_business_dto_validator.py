from ed_core.application.features.business.dtos.create_business_dto import \
    CreateBusinessDto
from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.validators.create_driver_dto_validator import \
    CreateLocationDtoValidator


class CreateBusinessDtoValidator(ABCDtoValidator[CreateBusinessDto]):
    def validate(self, dto: CreateBusinessDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if not dto["business_name"]:
            errors.append("Business name is required")

        if not dto["owner_first_name"]:
            errors.append("Business owner first name is required")

        if not dto["owner_last_name"]:
            errors.append("Business owner last name is required")

        if not dto["phone_number"]:
            errors.append("Phone number is required")

        if not dto["email"]:
            errors.append("Email is required")

        if not dto["billing_details"]:
            errors.append("Billing details is required")

        errors.extend(
            CreateLocationDtoValidator().validate(dto["location"]).errors,
        )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
