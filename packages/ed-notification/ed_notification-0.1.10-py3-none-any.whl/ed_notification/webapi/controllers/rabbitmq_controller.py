from typing import Annotated

from ed_domain.common.logging import get_logger
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit.schemas import RabbitQueue
from rmediator.mediator import Mediator

from ed_notification.application.features.notification.dtos.send_notification_dto import \
    SendNotificationDto
from ed_notification.application.features.notification.requests.commands.send_notification_command import \
    SendNotificationCommand
from ed_notification.common.generic_helpers import get_config
from ed_notification.webapi.dependency_setup import get_mediator

LOG = get_logger()

config = get_config()
router = RabbitRouter(config["rabbitmq"]["url"])
queue = RabbitQueue(name=config["rabbitmq"]["queue"], durable=True)


@router.subscriber(queue)
async def send_notification(
    message: SendNotificationDto,
    mediator: Annotated[Mediator, Depends(get_mediator)],
):
    LOG.info(f"Received message: {message}")
    return await mediator.send(SendNotificationCommand(dto=message))
