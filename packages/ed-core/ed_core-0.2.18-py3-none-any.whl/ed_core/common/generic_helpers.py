import os
import uuid

from dotenv import load_dotenv

from ed_core.common.typing.config import Config, Environment


def get_new_id() -> uuid.UUID:
    return uuid.uuid4()


def get_config() -> Config:
    load_dotenv()

    return {
        "mongo_db_connection_string": os.getenv("CONNECTION_STRING") or "",
        "db_name": os.getenv("DB_NAME") or "",
        "rabbitmq_url": os.getenv("RABBITMQ_URL") or "",
        "rabbitmq_queue": os.getenv("RABBITMQ_QUEUE") or "",
        "cloudinary": {
            "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME") or "",
            "api_key": os.getenv("CLOUDINARY_API_KEY") or "",
            "api_secret": os.getenv("CLOUDINARY_API_SECRET") or "",
            "env_variable": os.getenv("CLOUDINARY_ENV_VARIABLE") or "",
        },
        "auth_api": os.getenv("AUTH_API") or "",
        "notification_api": os.getenv("NOTIFICATION_API") or "",
        "environment": (
            Environment.PROD
            if os.getenv("ENVIRONMENT") == "production"
            else Environment.DEV
        ),
    }
