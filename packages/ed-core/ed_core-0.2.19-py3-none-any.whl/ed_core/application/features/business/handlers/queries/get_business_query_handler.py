from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.requests.queries import \
    GetBusinessQuery
from ed_core.application.features.common.dtos import BusinessDto


@request_handler(GetBusinessQuery, BaseResponse[BusinessDto])
class GetBusinessQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetBusinessQuery) -> BaseResponse[BusinessDto]:
        if business := self._uow.business_repository.get(id=request.business_id):
            return BaseResponse[BusinessDto].success(
                "Business fetched successfully.",
                BusinessDto.from_business(business, self._uow),
            )

        return BaseResponse[BusinessDto].error(
            "Business not found.",
            [f"Buisness with id {request.business_id} not found."],
        )
