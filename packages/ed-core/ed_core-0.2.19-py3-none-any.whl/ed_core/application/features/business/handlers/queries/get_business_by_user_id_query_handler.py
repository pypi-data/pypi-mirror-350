from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.requests.queries.get_business_by_user_id_query import \
    GetBusinessByUserIdQuery
from ed_core.application.features.common.dtos.business_dto import BusinessDto


@request_handler(GetBusinessByUserIdQuery, BaseResponse[BusinessDto])
class GetBusinessByUserIdQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetBusinessByUserIdQuery
    ) -> BaseResponse[BusinessDto]:
        if business := self._uow.business_repository.get(user_id=request.user_id):
            return BaseResponse[BusinessDto].success(
                "Business fetched successfully.",
                BusinessDto.from_business(business, self._uow),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Business not found.",
            [f"Buisness with user id {request.user_id} not found."],
        )
