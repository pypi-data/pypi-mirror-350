from typing import TypedDict


class Config(TypedDict):
    mongo_db_connection_string: str
    db_name: str
    rabbitmq_url: str
    rabbitmq_queue: str
    core_api: str


class TestMessage(TypedDict):
    title: str
