from datetime import datetime
from uuid import UUID

from ed_domain.core.entities.notification import Notification, NotificationType
from pydantic import BaseModel


class NotificationDto(BaseModel):
    id: UUID
    user_id: UUID
    notification_type: NotificationType
    message: str
    read_status: bool
    create_datetime: datetime

    @classmethod
    def from_notification(cls, notification: Notification) -> "NotificationDto":
        return cls(
            id=notification["id"],
            user_id=notification["user_id"],
            notification_type=notification["notification_type"],
            message=notification["message"],
            read_status=notification["read_status"],
            create_datetime=notification["create_datetime"],
        )
