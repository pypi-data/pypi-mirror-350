import os
from uuid import UUID, uuid4

from dotenv import load_dotenv

from ed_notification.common.typing.config import Config


def get_new_id() -> UUID:
    return uuid4()


def get_config() -> Config:
    load_dotenv()

    return {
        "resend": {
            "api_key": os.getenv("RESEND_API_KEY") or "",
            "from_email": os.getenv("RESEND_FROM_EMAIL") or "",
        },
        "mongo_db_connection_string": os.getenv("MONGO_DB_KEY") or "",
        "db_name": os.getenv("DB_NAME") or "",
        "infobig_key": os.getenv("INFOBIG_KEY") or "",
        "rabbitmq": {
            "url": os.getenv("RABBITMQ_URL") or "",
            "queue": os.getenv("RABBITMQ_QUEUE") or "",
        },
    }
