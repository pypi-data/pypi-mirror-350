from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain.core.entities.notification import NotificationType


class NotificationDto(TypedDict):
    id: UUID
    notification_type: NotificationType
    message: str
    read_status: bool
    create_datetime: datetime
    update_datetime: datetime
