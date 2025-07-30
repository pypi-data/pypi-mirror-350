from datetime import UTC, datetime

from ed_domain.core.entities.order import ParcelSize

from ed_core.application.features.business.dtos.create_orders_dto import (
    CreateConsumerDto, CreateOrderDto, CreateOrdersDto)
from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.validators.create_driver_dto_validator import \
    CreateLocationDtoValidator


class CreateConsumerDtoValidator(ABCDtoValidator[CreateConsumerDto]):
    def validate(self, dto: CreateConsumerDto) -> ValidationResponse:
        errors = []

        if not dto["first_name"]:
            errors.append("First name of consmer is required.")

        if not dto["last_name"]:
            errors.append("Last name of consmer is required.")

        if not dto["phone_number"]:
            errors.append("Phone number of consmer is required")

        errors.extend(
            CreateLocationDtoValidator().validate(dto["location"]).errors,
        )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()


class CreateOrderDtoValidator(ABCDtoValidator[CreateOrderDto]):
    def validate(self, dto: CreateOrderDto) -> ValidationResponse:
        consumer_dto_validation = CreateConsumerDtoValidator().validate(dto["consumer"])
        errors = consumer_dto_validation.errors

        print(dto["latest_time_of_delivery"], datetime.now(UTC))
        if dto["latest_time_of_delivery"] <= datetime.now(UTC):
            errors.append("Latest time of delivery must be in the future.")

        if dto["parcel"]["weight"] <= 0:
            errors.append("Weight of parcel is required.")

        if dto["parcel"]["dimensions"]["height"] <= 0:
            errors.append("Height dimension of parcel is required.")

        if dto["parcel"]["dimensions"]["width"] <= 0:
            errors.append("Width dimension of parcel is required.")

        if dto["parcel"]["dimensions"]["length"] <= 0:
            errors.append("Length dimension of parcel is required.")

        if not isinstance(dto["parcel"]["size"], ParcelSize):
            errors.append(
                f"Parcel size has to be one of {ParcelSize.SMALL}, {ParcelSize.MEDIUM} or {ParcelSize.LARGE}."
            )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()


class CreateOrdersDtoValidator(ABCDtoValidator[CreateOrdersDto]):
    def validate(self, dto: CreateOrdersDto) -> ValidationResponse:
        errors = []
        for order in dto["orders"]:
            order_dto_validation = CreateOrderDtoValidator().validate(order)
            errors.extend(order_dto_validation.errors)

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
