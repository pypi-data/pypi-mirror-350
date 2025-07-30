from uuid import UUID

from ed_domain.documentation.common.base_endpoint import BaseEndpoint
from ed_domain.documentation.common.endpoint_description import \
    EndpointDescription
from ed_domain.documentation.common.http_method import HttpMethod

from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto, UpdateNotificationDto)


class NotificationEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            {
                "name": "send_notification",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/notifications",
                "request_model": SendNotificationDto,
                "response_model": NotificationDto,
            },
            {
                "name": "get_notification_by_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/notifications/{{notification_id}}",
                "path_params": {"notification_id": UUID},
                "response_model": NotificationDto,
            },
            {
                "name": "update_notification",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/notifications/{{notification_id}}",
                "path_params": {"notification_id": UUID},
                "request_model": UpdateNotificationDto,
                "response_model": NotificationDto,
            },
            {
                "name": "get_notifications_for_user",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/notifications/users/{{user_id}}",
                "path_params": {"user_id": UUID},
                "response_model": list[NotificationDto],
            },
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions
