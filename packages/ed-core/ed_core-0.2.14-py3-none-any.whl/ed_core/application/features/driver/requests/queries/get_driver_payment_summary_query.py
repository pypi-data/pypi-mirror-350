from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.types import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.driver.dtos import DriverPaymentSummaryDto


@request(BaseResponse[DriverPaymentSummaryDto])
@dataclass
class GetDriverPaymentSummaryQuery(Request):
    driver_id: UUID
