from uuid import UUID

from ed_domain.documentation.api.definitions import ApiResponse
from ed_infrastructure.documentation.api.endpoint_client import EndpointClient

from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto, UpdateNotificationDto)
from ed_notification.documentation.api.abc_notification_api_client import \
    ABCNotificationApiClient
from ed_notification.documentation.api.notification_endpoint_descriptions import \
    NotificationEndpointDescriptions


class NotificationApiClient(ABCNotificationApiClient):
    def __init__(self, auth_api: str) -> None:
        self._notification_endpoints = NotificationEndpointDescriptions(
            auth_api)

    def send_notification(
        self, send_notification_dto: SendNotificationDto
    ) -> ApiResponse[NotificationDto]:
        endpoint = self._notification_endpoints.get_description(
            "send_notification")

        api_client = EndpointClient[NotificationDto](endpoint)

        return api_client({"request": send_notification_dto})

    def get_notification_by_id(
        self, notification_id: UUID
    ) -> ApiResponse[NotificationDto]:
        endpoint = self._notification_endpoints.get_description(
            "get_notification_by_id"
        )

        api_client = EndpointClient[NotificationDto](endpoint)

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

        api_client = EndpointClient[NotificationDto](endpoint)

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

        api_client = EndpointClient[list[NotificationDto]](endpoint)

        return api_client(
            {
                "path_params": {
                    "user_id": user_id,
                }
            }
        )
