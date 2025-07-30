from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.dtos import UpdateBusinessDto
from ed_core.application.features.common.dtos.business_dto import BusinessDto


@request(BaseResponse[BusinessDto])
@dataclass
class UpdateBusinessCommand(Request):
    id: UUID
    dto: UpdateBusinessDto
