from typing import Annotated

from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.queues.common.abc_producer import ABCProducer
from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.unit_of_work import UnitOfWork
from ed_infrastructure.queues.rabbitmq.producer import RabbitMQProducer
from fastapi import Depends
from rmediator.mediator import Mediator

from ed_optimization.application.contracts.infrastructure.api.abc_api import \
    ABCApi
from ed_optimization.application.contracts.infrastructure.cache.abc_cache import \
    ABCCache
from ed_optimization.application.features.order.handlers.commands.process_order_command_handler import \
    ProcessOrderCommandHandler
from ed_optimization.application.features.order.requests.commands.process_order_command import \
    ProcessOrderCommand
from ed_optimization.common.generic_helpers import get_config
from ed_optimization.common.typing.config import Config, TestMessage
from ed_optimization.infrastructure.api.api_handler import ApiHandler
from ed_optimization.infrastructure.cache.in_memory_cache import InMemoryCache


def get_db_client(config: Annotated[Config, Depends(get_config)]) -> DbClient:
    return DbClient(
        config["mongo_db_connection_string"],
        config["db_name"],
    )


def get_cache() -> ABCCache:
    return InMemoryCache()


def get_uow(db_client: Annotated[DbClient, Depends(get_db_client)]) -> ABCUnitOfWork:
    return UnitOfWork(db_client)


def get_producer(config: Annotated[Config, Depends(get_config)]) -> ABCProducer:
    producer = RabbitMQProducer[TestMessage](
        config["rabbitmq_url"],
        config["rabbitmq_queue"],
    )
    producer.start()

    return producer


def get_api(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return ApiHandler(config["core_api"])


def mediator(
    uow: Annotated[ABCUnitOfWork, Depends(get_uow)],
    producer: Annotated[ABCProducer, Depends(get_producer)],
    cache: Annotated[ABCCache, Depends(get_cache)],
    api: Annotated[ABCApi, Depends(get_api)],
) -> Mediator:
    mediator = Mediator()

    handlers = [
        (
            ProcessOrderCommand,
            ProcessOrderCommandHandler(uow, producer, cache, api),
        )
    ]
    for command, handler in handlers:
        mediator.register_handler(command, handler)

    return mediator
