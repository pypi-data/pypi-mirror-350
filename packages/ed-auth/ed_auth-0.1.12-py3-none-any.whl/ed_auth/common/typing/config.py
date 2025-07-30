from enum import StrEnum
from typing import TypedDict


class Environment(StrEnum):
    TEST = "test"
    DEV = "development"
    STAGING = "staging"
    PROD = "prod"


class DBConfig(TypedDict):
    mongo_db_connection_string: str
    db_name: str


class RabbitMQConfig(TypedDict):
    url: str
    queue: str


class JwtConfig(TypedDict):
    secret: str
    algorithm: str


class Config(TypedDict):
    db: DBConfig
    rabbitmq: RabbitMQConfig
    jwt: JwtConfig
    password_scheme: str
    env: Environment
    notification_api: str


class TestMessage(TypedDict):
    title: str
