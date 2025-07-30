from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.types import Request

from ed_notification.application.common.responses.base_response import \
    BaseResponse
from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto)


@request(BaseResponse[NotificationDto])
@dataclass
class SendNotificationCommand(Request):
    dto: SendNotificationDto
