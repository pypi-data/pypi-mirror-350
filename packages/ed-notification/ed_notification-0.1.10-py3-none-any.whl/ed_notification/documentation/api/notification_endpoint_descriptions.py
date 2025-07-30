from uuid import UUID

from ed_domain.documentation.api.abc_endpoint_descriptions import \
    ABCEndpointDescriptions
from ed_domain.documentation.api.definitions import (EndpointDescription,
                                                     HttpMethod)

from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto, UpdateNotificationDto)


class NotificationEndpointDescriptions(ABCEndpointDescriptions):
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
