from dataclasses import dataclass

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import ConsumerDto
from ed_core.application.features.consumer.requests.queries.get_consumer_query import \
    GetConsumerQuery


@request_handler(GetConsumerQuery, BaseResponse[ConsumerDto])
@dataclass
class GetConsumerQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetConsumerQuery) -> BaseResponse[ConsumerDto]:
        if consumer := self._uow.consumer_repository.get(id=request.consumer_id):
            return BaseResponse[ConsumerDto].success(
                "Consumer fetched successfully.",
                ConsumerDto.from_consumer(consumer, self._uow),
            )

        return BaseResponse[ConsumerDto].error(
            "Consumer couldn't be fetched.",
            [f"Consumer with id {request.consumer_id} does not exist."],
        )
