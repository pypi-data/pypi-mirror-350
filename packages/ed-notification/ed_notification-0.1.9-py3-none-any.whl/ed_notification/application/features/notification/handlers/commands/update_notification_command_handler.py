from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_notification.application.common.responses.base_response import \
    BaseResponse
from ed_notification.application.features.notification.dtos import (
    NotificationDto, UpdateNotificationDto)
from ed_notification.application.features.notification.requests.commands import \
    UpdateNotificationCommand
from ed_notification.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateNotificationCommand, BaseResponse[NotificationDto])
class UpdateNotificationCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: UpdateNotificationCommand
    ) -> BaseResponse[NotificationDto]:
        notification_id = request.notification_id
        dto: UpdateNotificationDto = request.dto

        if notification := self._uow.notification_repository.get(id=notification_id):
            notification["read_status"] = dto["read_status"]
            if self._uow.notification_repository.update(notification_id, notification):
                return BaseResponse[NotificationDto].success(
                    "Notification updated successfully.",
                    NotificationDto(**notification),  # type: ignore
                )

            return BaseResponse[NotificationDto].error(
                "Notification not updated.",
                ["Notification cannot be updated with the given data."],
            )

        return BaseResponse[NotificationDto].error(
            "Notification not updated.",
            [f"Notification with id = {notification_id} not found."],
        )
