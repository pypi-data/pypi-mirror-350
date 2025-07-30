from typing import TypedDict


class DbConfig(TypedDict):
    connection_string: str
    db_name: str


class RabbitMQConfig(TypedDict):
    url: str
    queue: str


class Config(TypedDict):
    db: DbConfig
    rabbitmq: RabbitMQConfig
    core_api: str


class TestMessage(TypedDict):
    title: str
