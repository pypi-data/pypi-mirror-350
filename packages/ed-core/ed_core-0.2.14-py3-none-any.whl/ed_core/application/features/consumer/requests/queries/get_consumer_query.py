from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import ConsumerDto


@request(BaseResponse[ConsumerDto])
@dataclass
class GetConsumerQuery(Request):
    consumer_id: UUID
