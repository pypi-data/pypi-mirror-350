import os
import uuid

from dotenv import load_dotenv

from ed_optimization.common.typing.config import Config


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
            "queue": _get_env_variable("RABBITMQ_QUEUE"),
        },
        "core_api": _get_env_variable("CORE_API"),
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
