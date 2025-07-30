import os
import uuid

from dotenv import load_dotenv
from ed_domain.common.logging import get_logger

from ed_auth.common.typing.config import Config, Environment

LOG = get_logger()


def get_new_id() -> uuid.UUID:
    return uuid.uuid4()


def get_config() -> Config:
    load_dotenv()

    config = {
        "db": {
            "mongo_db_connection_string": os.getenv("CONNECTION_STRING") or "",
            "db_name": os.getenv("DB_NAME") or "",
        },
        "rabbitmq": {
            "url": os.getenv("RABBITMQ_URL") or "",
            "queue": os.getenv("RABBITMQ_QUEUE") or "",
        },
        "jwt": {
            "secret": os.getenv("JWT_SECRET") or "",
            "algorithm": os.getenv("JWT_ALGORITHM") or "",
        },
        "password_scheme": os.getenv("PASSWORD_SCHEME") or "",
        "env": Environment.PROD if os.getenv("ENV") == "prod" else Environment.DEV,
        "notification_api": os.getenv("NOTIFICATION_API") or "",
    }

    print("Configuration loaded:", config)
    return Config(**config)
