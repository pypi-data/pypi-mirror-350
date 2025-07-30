from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.consumer.dtos.update_consumer_dto import (
    UpdateConsumerDto, UpdateLocationDto)


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


class UpdateConsumerDtoValidator(ABCDtoValidator[UpdateConsumerDto]):
    def validate(self, dto: UpdateConsumerDto) -> ValidationResponse:
        errors = []
        if "location" in dto:
            errors.extend(
                UpdateLocationDtoValidator().validate(dto["location"]).errors,
            )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
