from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.update_driver_dto import (
    UpdateCarDto, UpdateDriverDto, UpdateLocationDto)


class UpdateLocationDtoValidator(ABCDtoValidator[UpdateLocationDto]):
    def validate(self, dto: UpdateLocationDto) -> ValidationResponse:
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


class UpdateCarDtoValidator(ABCDtoValidator[UpdateCarDto]):
    def validate(self, dto: UpdateCarDto) -> ValidationResponse:
        errors = []

        if not dto.get("model"):
            errors.append("Model is required")

        if not dto["make"]:
            errors.append("Make is required")

        if not dto["year"]:
            errors.append("Year is required")

        if not dto["color"]:
            errors.append("Color is required")

        if not dto["license_plate"]:
            errors.append("License plate is required")

        if not dto["seats"]:
            errors.append("Seats is required")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()


class UpdateDriverDtoValidator(ABCDtoValidator[UpdateDriverDto]):
    def validate(self, dto: UpdateDriverDto) -> ValidationResponse:
        errors = []
        if "location" in dto:
            errors.extend(
                UpdateLocationDtoValidator().validate(dto["location"]).errors,
            )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
