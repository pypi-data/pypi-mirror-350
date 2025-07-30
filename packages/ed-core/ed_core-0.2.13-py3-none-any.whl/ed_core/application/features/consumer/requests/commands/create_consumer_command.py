from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import ConsumerDto
from ed_core.application.features.consumer.dtos import CreateConsumerDto


@request(BaseResponse[ConsumerDto])
@dataclass
class CreateConsumerCommand(Request):
    dto: CreateConsumerDto
