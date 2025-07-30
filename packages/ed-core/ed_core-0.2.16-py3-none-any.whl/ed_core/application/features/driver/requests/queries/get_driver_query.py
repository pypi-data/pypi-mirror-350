from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DriverDto


@request(BaseResponse[DriverDto])
@dataclass
class GetDriverQuery(Request):
    driver_id: UUID
