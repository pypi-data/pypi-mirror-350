from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos.business_dto import BusinessDto


@request(BaseResponse[BusinessDto])
@dataclass
class GetBusinessByUserIdQuery(Request):
    user_id: UUID
