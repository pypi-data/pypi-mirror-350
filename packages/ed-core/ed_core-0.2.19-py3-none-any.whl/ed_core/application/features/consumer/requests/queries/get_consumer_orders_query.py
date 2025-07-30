from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.types import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import OrderDto


@request(BaseResponse[list[OrderDto]])
@dataclass
class GetConsumerOrdersQuery(Request):
    consumer_id: UUID
