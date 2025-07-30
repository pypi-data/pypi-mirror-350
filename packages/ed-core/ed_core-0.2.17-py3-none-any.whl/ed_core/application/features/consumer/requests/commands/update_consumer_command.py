from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import ConsumerDto
from ed_core.application.features.consumer.dtos import UpdateConsumerDto


@request(BaseResponse[ConsumerDto])
@dataclass
class UpdateConsumerCommand(Request):
    consumer_id: UUID
    dto: UpdateConsumerDto
