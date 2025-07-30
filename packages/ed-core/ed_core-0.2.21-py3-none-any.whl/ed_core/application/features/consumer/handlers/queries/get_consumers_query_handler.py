from dataclasses import dataclass

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import ConsumerDto
from ed_core.application.features.consumer.requests.queries import \
    GetConsumersQuery


@request_handler(GetConsumersQuery, BaseResponse[list[ConsumerDto]])
@dataclass
class GetConsumersQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetConsumersQuery
    ) -> BaseResponse[list[ConsumerDto]]:
        if consumers := self._uow.consumer_repository.get_all():
            return BaseResponse[list[ConsumerDto]].success(
                "Consumers fetched successfully.",
                [
                    ConsumerDto.from_consumer(consumer, self._uow)
                    for consumer in consumers
                ],
            )

        return BaseResponse[list[ConsumerDto]].error(
            "Consumers couldn't be fetched.", ["There are no consumers."]
        )
