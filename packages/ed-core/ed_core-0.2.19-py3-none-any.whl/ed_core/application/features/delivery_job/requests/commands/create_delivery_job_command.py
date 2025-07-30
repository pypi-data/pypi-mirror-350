from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.types import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DeliveryJobDto
from ed_core.application.features.delivery_job.dtos import CreateDeliveryJobDto


@request(BaseResponse[DeliveryJobDto])
@dataclass
class CreateDeliveryJobCommand(Request):
    dto: CreateDeliveryJobDto
