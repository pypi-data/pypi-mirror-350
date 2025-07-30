from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.consumer.dtos.create_consumer_dto import (
    CreateConsumerDto, CreateLocationDto)


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


class CreateConsumerDtoValidator(ABCDtoValidator[CreateConsumerDto]):
    def validate(self, dto: CreateConsumerDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if not dto["first_name"]:
            errors.append("First name is required")

        if not dto["last_name"]:
            errors.append("Last name is required")

        if not dto["phone_number"]:
            errors.append("Phone number is required")

        errors.extend(
            CreateLocationDtoValidator().validate(dto["location"]).errors,
        )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
