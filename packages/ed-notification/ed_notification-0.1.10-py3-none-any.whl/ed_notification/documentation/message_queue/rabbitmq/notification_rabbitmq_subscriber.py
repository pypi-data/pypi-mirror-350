from ed_infrastructure.documentation.message_queue.rabbitmq.rabbitmq_producer import \
    RabbitMQProducer

from ed_notification.application.features.notification.dtos.send_notification_dto import \
    SendNotificationDto
from ed_notification.documentation.message_queue.rabbitmq.abc_notification_rabbitmq_subscriber import \
    ABCNotificationRabbitMQSubscriber
from ed_notification.documentation.message_queue.rabbitmq.notification_queue_descriptions import \
    NotificationQueueDescriptions


class NotificationRabbitMQSubscriber(ABCNotificationRabbitMQSubscriber):
    def __init__(self, connection_url: str) -> None:
        self._connection_url = connection_url
        self._queues = NotificationQueueDescriptions(connection_url)

    def send_notification(self, send_notification_dto: SendNotificationDto) -> None:
        queue = self._queues.get_queue("notification")
        producer = RabbitMQProducer[SendNotificationDto](
            queue["connection_parameters"]["url"],
            queue["connection_parameters"]["queue"],
        )
        producer.start()
        producer.publish(send_notification_dto)
        producer.stop()
