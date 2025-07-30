from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.types import Request

from ed_notification.application.common.responses.base_response import \
    BaseResponse
from ed_notification.application.features.notification.dtos import (
    NotificationDto, UpdateNotificationDto)


@request(BaseResponse[NotificationDto])
@dataclass
class UpdateNotificationCommand(Request):
    notification_id: UUID
    dto: UpdateNotificationDto
