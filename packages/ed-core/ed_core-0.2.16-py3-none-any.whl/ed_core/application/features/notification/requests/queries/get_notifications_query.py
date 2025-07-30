from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.types import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import NotificationDto


@request(BaseResponse[list[NotificationDto]])
@dataclass
class GetNotificationsQuery(Request):
    user_id: UUID
