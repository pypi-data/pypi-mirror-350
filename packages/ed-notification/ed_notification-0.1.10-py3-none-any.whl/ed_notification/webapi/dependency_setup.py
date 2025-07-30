from typing import Annotated

from ed_domain.core.repositories import ABCUnitOfWork
from ed_domain.utils.email.abc_email_sender import ABCEmailSender
from ed_domain.utils.sms.abc_sms_sender import ABCSmsSender
from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.unit_of_work import UnitOfWork
from ed_infrastructure.utils.email.email_sender import EmailSender
from ed_infrastructure.utils.sms.sms_sender import SmsSender
from fastapi import Depends
from rmediator.mediator import Mediator

from ed_notification.application.features.notification.handlers.commands import (
    SendNotificationCommandHandler, UpdateNotificationCommandHandler)
from ed_notification.application.features.notification.handlers.queries import (
    GetNotificationQueryHandler, GetNotificationsQueryHandler)
from ed_notification.application.features.notification.requests.commands import (
    SendNotificationCommand, UpdateNotificationCommand)
from ed_notification.application.features.notification.requests.queries import (
    GetNotificationQuery, GetNotificationsQuery)
from ed_notification.common.generic_helpers import get_config
from ed_notification.common.typing.config import Config


def email_sender(config: Annotated[Config, Depends(get_config)]) -> ABCEmailSender:
    return EmailSender(config["resend"]["api_key"])


def sms_sender(config: Annotated[Config, Depends(get_config)]) -> ABCSmsSender:
    return SmsSender(config["infobig_key"])


def db_client(config: Annotated[Config, Depends(get_config)]) -> DbClient:
    db_client = DbClient(
        config["mongo_db_connection_string"], config["db_name"])
    db_client.start()

    return db_client


def unit_of_work(
    db_client: Annotated[DbClient, Depends(db_client)],
) -> ABCUnitOfWork:
    return UnitOfWork(db_client)


def get_mediator(
    config: Annotated[Config, Depends(get_config)],
    uow: Annotated[ABCUnitOfWork, Depends(unit_of_work)],
    email_sender: Annotated[ABCEmailSender, Depends(email_sender)],
    sms_sender: Annotated[ABCSmsSender, Depends(sms_sender)],
) -> Mediator:
    # Setup
    mediator = Mediator()

    requests_and_handlers = [
        (
            SendNotificationCommand,
            SendNotificationCommandHandler(
                config["resend"], uow, email_sender, sms_sender
            ),
        ),
        (
            UpdateNotificationCommand,
            UpdateNotificationCommandHandler(uow),
        ),
        (GetNotificationQuery, GetNotificationQueryHandler(uow)),
        (GetNotificationsQuery, GetNotificationsQueryHandler(uow)),
    ]

    for request, handler in requests_and_handlers:
        mediator.register_handler(request, handler)

    return mediator


if __name__ == "__main__":
    import asyncio

    async def main():
        sender = email_sender(get_config())
        email = await sender.send(
            sender="Support <support@easydrop-et.space>",
            recipient="phikernew0808@gmail.com",
            subject="From support",
            html="<p>it works!</p>",
        )
        print(email)

    asyncio.run(main())
