from typing import TypedDict


class RabbitMQConfig(TypedDict):
    url: str
    queue: str


class ResendConfig(TypedDict):
    api_key: str
    from_email: str


class Config(TypedDict):
    resend: ResendConfig
    infobig_key: str
    mongo_db_connection_string: str
    db_name: str
    rabbitmq: RabbitMQConfig


class TestMessage(TypedDict):
    title: str
