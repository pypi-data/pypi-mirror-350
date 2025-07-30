from abc import ABCMeta, abstractmethod
from uuid import UUID

from ed_domain.documentation.common.api_response import ApiResponse

from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto, UpdateNotificationDto)


class ABCNotificationApiClient(metaclass=ABCMeta):
    @abstractmethod
    def send_notification(
        self, send_notification_dto: SendNotificationDto
    ) -> ApiResponse[NotificationDto]: ...

    @abstractmethod
    def get_notification_by_id(
        self, notification_id: UUID
    ) -> ApiResponse[NotificationDto]: ...

    @abstractmethod
    def update_notification(
        self, notification_id: UUID, update_dto: UpdateNotificationDto
    ) -> ApiResponse[NotificationDto]: ...

    @abstractmethod
    def get_notifications_for_user(
        self, user_id: UUID
    ) -> ApiResponse[list[NotificationDto]]: ...
