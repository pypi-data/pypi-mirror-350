from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_core.application.features.common.dtos import NotificationDto
from ed_core.application.features.notification.requests.queries import \
    GetNotificationsQuery
from ed_core.common.logging_helpers import get_logger
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/notifications", tags=["Notification Feature"])


@router.get("/users/{user_id}", response_model=GenericResponse[list[NotificationDto]])
@rest_endpoint
async def get_user_notifications(
    user_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetNotificationsQuery(user_id=user_id))
