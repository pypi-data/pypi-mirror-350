from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import NotificationDto
from ed_core.application.features.notification.requests.queries import \
    GetNotificationsQuery


@request_handler(GetNotificationsQuery, BaseResponse[list[NotificationDto]])
class GetNotificationsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetNotificationsQuery
    ) -> BaseResponse[list[NotificationDto]]:
        notifications = self._uow.notification_repository.get_all(
            user_id=request.user_id
        )
        return BaseResponse[list[NotificationDto]].success(
            "Notifications fetched successfully.",
            [
                NotificationDto.from_notification(notification)
                for notification in notifications
            ],
        )
