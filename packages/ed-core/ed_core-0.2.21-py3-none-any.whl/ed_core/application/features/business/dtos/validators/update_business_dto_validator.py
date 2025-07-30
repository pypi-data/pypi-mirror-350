from ed_core.application.features.business.dtos.update_business_dto import \
    UpdateBusinessDto
from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.validators.create_driver_dto_validator import \
    CreateLocationDtoValidator


class UpdateBusinessDtoValidator(ABCDtoValidator[UpdateBusinessDto]):
    _location_validator = CreateLocationDtoValidator()

    def validate(self, dto: UpdateBusinessDto) -> ValidationResponse:
        errors = []

        if "location" in dto:
            errors.extend(
                self._location_validator.validate(dto["location"]).errors,
            )

        # Add validation for other fields in UpdateBusinessDto
        # For example:
        # if "name" in dto and not dto["name"]:
        #     errors.append("Business name cannot be empty")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
