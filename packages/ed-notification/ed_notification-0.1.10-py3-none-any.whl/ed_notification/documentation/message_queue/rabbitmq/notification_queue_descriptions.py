from ed_domain.documentation.message_queue.rabbitmq.abc_queue_descriptions import \
    ABCQueueDescriptions
from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription

from ed_notification.application.features.notification.dtos.send_notification_dto import \
    SendNotificationDto


class NotificationQueueDescriptions(ABCQueueDescriptions):
    def __init__(self, connection_url: str) -> None:
        self._descriptions: list[QueueDescription] = [
            {
                "name": "send_notification",
                "connection_parameters": {
                    "url": connection_url,
                    "queue": "notification",
                },
                "durable": True,
                "request_model": SendNotificationDto,
            }
        ]

    @property
    def descriptions(self) -> list[QueueDescription]:
        return self._descriptions
