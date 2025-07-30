from abc import ABCMeta, abstractmethod

from ed_notification.application.features.notification.dtos.send_notification_dto import \
    SendNotificationDto


class ABCNotificationRabbitMQSubscriber(metaclass=ABCMeta):
    @abstractmethod
    def send_notification(
        self, send_notification_dto: SendNotificationDto) -> None: ...
