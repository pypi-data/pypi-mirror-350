from dataclasses import dataclass

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import ConsumerDto
from ed_core.application.features.consumer.requests.queries import \
    GetConsumerByUserIdQuery


@request_handler(GetConsumerByUserIdQuery, BaseResponse[ConsumerDto])
@dataclass
class GetConsumerByUserIdQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetConsumerByUserIdQuery
    ) -> BaseResponse[ConsumerDto]:
        if consumer := self._uow.consumer_repository.get(user_id=request.user_id):
            return BaseResponse[ConsumerDto].success(
                "Consumer fetched successfully.",
                ConsumerDto.from_consumer(consumer, self._uow),
            )

        return BaseResponse[ConsumerDto].error(
            "Consumer couldn't be fetched.",
            [f"Consumer with user id {request.user_id} not found."],
        )
