from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.types import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DeliveryJobDto


@request(BaseResponse[DeliveryJobDto])
@dataclass
class GetDeliveryJobQuery(Request):
    delivery_job_id: UUID
