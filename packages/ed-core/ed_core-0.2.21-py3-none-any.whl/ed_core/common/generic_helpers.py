import os
import uuid

from dotenv import load_dotenv

from ed_core.common.typing.config import Config, Environment


def get_new_id() -> uuid.UUID:
    return uuid.uuid4()


def get_config() -> Config:
    load_dotenv()

    return {
        "db": {
            "connection_string": _get_env_variable("CONNECTION_STRING"),
            "db_name": _get_env_variable("DB_NAME"),
        },
        "rabbitmq": {
            "url": _get_env_variable("RABBITMQ_URL"),
            "queues": {
                "subscribe_create_delivery_job": _get_env_variable(
                    "RABBITMQ_QUEUE_SUBSCRIBE_CREATE_DELIVERY_JOB"
                ),
                "produce_notification": _get_env_variable(
                    "RABBITMQ_QUEUE_SEND_NOTIFICATION"
                ),
                "produce_order": _get_env_variable("RABBITMQ_QUEUE_SEND_NOTIFICATION"),
            },
        },
        "auth_api": _get_env_variable("AUTH_API"),
        "notification_api": _get_env_variable("NOTIFICATION_API"),
        "environment": (
            Environment.PROD
            if _get_env_variable("ENVIRONMENT") == "production"
            else Environment.DEV
        ),
    }


def _get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set.")

    if not isinstance(value, str):
        raise TypeError(f"Environment variable '{name}' must be a string.")

    value = value.strip()
    if not value:
        raise ValueError(f"Environment variable '{name}' cannot be empty.")

    return value
