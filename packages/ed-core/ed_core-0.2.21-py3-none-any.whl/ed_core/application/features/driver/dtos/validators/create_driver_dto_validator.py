from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.create_driver_dto import (
    CreateCarDto, CreateDriverDto, CreateLocationDto)


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


class CreateCarDtoValidator(ABCDtoValidator[CreateCarDto]):
    def validate(self, dto: CreateCarDto) -> ValidationResponse:
        errors = []

        if not dto["model"]:
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


class CreateDriverDtoValidator(ABCDtoValidator[CreateDriverDto]):
    def validate(self, dto: CreateDriverDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if not dto["first_name"]:
            errors.append("First name is required")

        if not dto["last_name"]:
            errors.append("Last name is required")

        if not dto["phone_number"]:
            errors.append("Phone number is required")

        if not dto["profile_image"]:
            errors.append("Profile image is required")

        errors.extend(
            CreateCarDtoValidator().validate(dto["car"]).errors,
        )
        errors.extend(
            CreateLocationDtoValidator().validate(dto["location"]).errors,
        )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
