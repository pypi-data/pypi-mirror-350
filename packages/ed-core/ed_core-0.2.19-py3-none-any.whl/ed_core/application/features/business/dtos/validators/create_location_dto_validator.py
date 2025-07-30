from ed_core.application.features.business.dtos.create_location_dto import \
    CreateLocationDto
from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class CreateLocationDtoValidator(ABCDtoValidator[CreateLocationDto]):
    def validate(self, dto: CreateLocationDto) -> ValidationResponse:
        errors = []

        if not dto["latitude"]:
            errors.append("Latitude is required")

        if not dto["longitude"]:
            errors.append("Longitude is required")

        if not dto["address"]:
            errors.append("Address is required")

        if not dto["postal_code"]:
            errors.append("Postal code is required")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
