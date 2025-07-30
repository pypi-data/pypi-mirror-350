from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities import Bill, Consumer, Location, Order
from ed_domain.core.entities.order import OrderStatus
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.core.value_objects.money import Currency, Money
from ed_domain.queues.ed_optimization.order_model import (BusinessModel,
                                                          ConsumerModel,
                                                          OrderModel)
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_core.application.features.business.dtos import CreateLocationDto
from ed_core.application.features.business.dtos.create_orders_dto import \
    CreateConsumerDto
from ed_core.application.features.business.dtos.validators.create_orders_dto_validator import \
    CreateOrdersDtoValidator
from ed_core.application.features.business.requests.commands import \
    CreateOrdersCommand
from ed_core.application.features.common.dtos import OrderDto
from ed_core.common.generic_helpers import get_new_id
from ed_core.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrdersCommand, BaseResponse[list[OrderDto]])
class CreateOrdersCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, api: ABCApi):
        self._uow = uow
        self._api = api

    async def handle(
        self, request: CreateOrdersCommand
    ) -> BaseResponse[list[OrderDto]]:
        business_id = request.business_id
        dto = request.dto
        dto_validator = CreateOrdersDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            return BaseResponse[list[OrderDto]].error(
                "Orders cannot be created.",
                dto_validator.errors,
            )

        consumers = [
            self._create_or_get_consumer(
                order["consumer"],
            )
            for order in dto["orders"]
        ]
        bill = self._create_bill()
        created_orders = self._uow.order_repository.create_many(
            [
                Order(
                    id=get_new_id(),
                    consumer_id=consumer["id"],
                    business_id=business_id,
                    bill_id=bill["id"],
                    latest_time_of_delivery=order["latest_time_of_delivery"],
                    parcel=order["parcel"],
                    order_status=OrderStatus.PENDING,
                    create_datetime=datetime.now(UTC),
                    update_datetime=datetime.now(UTC),
                    deleted=False,
                )
                for consumer, order in zip(consumers, dto["orders"])
            ]
        )

        self._publish_orders(created_orders, consumers)

        return BaseResponse[list[OrderDto]].success(
            "Order created successfully.",
            [OrderDto.from_order(order, self._uow) for order in created_orders],
        )

    def _create_or_get_consumer(self, consumer: CreateConsumerDto) -> Consumer:
        if existing_consumer := self._uow.consumer_repository.get(
            phone_number=consumer["phone_number"]
        ):
            return existing_consumer

        location = self._create_location(consumer["location"])
        create_user_response = self._api.auth_api.create_get_otp(
            {
                "first_name": consumer["first_name"],
                "last_name": consumer["last_name"],
                "phone_number": consumer["phone_number"],
                "email": consumer["email"],
            }
        )
        if not create_user_response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create orders",
                ["Could not create consumers."],
            )

        user = create_user_response["data"]

        new_consumer = Consumer(
            **consumer,  # type: ignore
            id=get_new_id(),
            user_id=user["id"],
            notification_ids=[],
            active_status=True,
            created_datetime=datetime.now(UTC),
            updated_datetime=datetime.now(UTC),
            location_id=location["id"],
        )

        return self._uow.consumer_repository.create(new_consumer)

    def _create_location(self, location: CreateLocationDto) -> Location:
        return self._uow.location_repository.create(
            Location(
                **location,
                id=get_new_id(),
                city="Addis Ababa",
                country="Ethiopia",
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
            )
        )

    def _create_bill(self) -> Bill:
        return self._uow.bill_repository.create(
            Bill(
                id=get_new_id(),
                amount=Money(
                    amount=10,
                    currency=Currency.ETB,
                ),
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
                paid=False,
            )
        )

    def _publish_orders(self, orders: list[Order], consumers: list[Consumer]) -> None:
        for order, consumer in zip(orders, consumers):
            self._producer.publish(
                OrderModel(
                    **order,  # type: ignore
                    consumer=ConsumerModel(**consumer),  # type: ignore
                    business=BusinessModel(
                        **self._uow.business_repository.get(
                            id=order["business_id"],
                        )  # type: ignore
                    ),
                )
            )
