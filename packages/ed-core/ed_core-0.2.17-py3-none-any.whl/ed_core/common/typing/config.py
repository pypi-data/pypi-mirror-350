from enum import StrEnum
from typing import TypedDict


class CloudinaryConfig(TypedDict):
    cloud_name: str
    api_key: str
    api_secret: str
    env_variable: str


class Environment(StrEnum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
    TEST = "test"


class Config(TypedDict):
    mongo_db_connection_string: str
    db_name: str
    rabbitmq_url: str
    rabbitmq_queue: str
    cloudinary: CloudinaryConfig
    auth_api: str
    notification_api: str
    environment: Environment


class TestMessage(TypedDict):
    title: str
