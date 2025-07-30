from uuid import UUID

from ed_domain.documentation.common.api_response import ApiResponse

from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto, UpdateNotificationDto)
from ed_notification.common.api_helpers import ApiClient
from ed_notification.documentation.abc_notification_api_client import \
    ABCNotificationApiClient
from ed_notification.documentation.endpoints import NotificationEndpoint


class NotificationApiClient(ABCNotificationApiClient):
    def __init__(self, auth_api: str) -> None:
        self._notification_endpoints = NotificationEndpoint(auth_api)

    def send_notification(
        self, send_notification_dto: SendNotificationDto
    ) -> ApiResponse[NotificationDto]:
        endpoint = self._notification_endpoints.get_description(
            "send_notification")

        api_client = ApiClient[NotificationDto](endpoint)

        return api_client({"request": send_notification_dto})

    def get_notification_by_id(
        self, notification_id: UUID
    ) -> ApiResponse[NotificationDto]:
        endpoint = self._notification_endpoints.get_description(
            "get_notification_by_id"
        )

        api_client = ApiClient[NotificationDto](endpoint)

        return api_client(
            {
                "path_params": {
                    "notification_id": notification_id,
                }
            }
        )

    def update_notification(
        self, notification_id: UUID, update_dto: UpdateNotificationDto
    ) -> ApiResponse[NotificationDto]:
        endpoint = self._notification_endpoints.get_description(
            "update_notification")

        api_client = ApiClient[NotificationDto](endpoint)

        return api_client(
            {
                "path_params": {
                    "notification_id": notification_id,
                },
                "request": update_dto,
            }
        )

    def get_notifications_for_user(
        self, user_id: UUID
    ) -> ApiResponse[list[NotificationDto]]:
        endpoint = self._notification_endpoints.get_description(
            "get_notifications_for_user"
        )

        api_client = ApiClient[list[NotificationDto]](endpoint)

        return api_client(
            {
                "path_params": {
                    "user_id": user_id,
                }
            }
        )
