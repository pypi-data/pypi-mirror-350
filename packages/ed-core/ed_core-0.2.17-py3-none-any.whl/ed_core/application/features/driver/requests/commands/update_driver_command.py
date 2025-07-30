from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import DriverDto
from ed_core.application.features.driver.dtos import UpdateDriverDto


@request(BaseResponse[DriverDto])
@dataclass
class UpdateDriverCommand(Request):
    driver_id: UUID
    dto: UpdateDriverDto
