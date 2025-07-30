from enum import StrEnum
from typing import TypedDict


class Environment(StrEnum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
    TEST = "test"


class RabbitMQConfig(TypedDict):
    url: str
    queues: dict[str, str]


class DbConfig(TypedDict):
    connection_string: str
    db_name: str


class Config(TypedDict):
    db: DbConfig
    rabbitmq: RabbitMQConfig
    auth_api: str
    notification_api: str
    environment: Environment
