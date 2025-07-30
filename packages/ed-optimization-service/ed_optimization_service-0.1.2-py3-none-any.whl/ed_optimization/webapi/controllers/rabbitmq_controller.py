from typing import Annotated

from ed_domain.queues.ed_optimization.order_model import OrderModel
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit.schemas import RabbitQueue
from rmediator.mediator import Mediator

from ed_optimization.application.features.order.requests.commands.process_order_command import \
    ProcessOrderCommand
from ed_optimization.common.generic_helpers import get_config
from ed_optimization.common.logging_helpers import get_logger
from ed_optimization.webapi.dependency_setup import mediator

config = get_config()
router = RabbitRouter(config["rabbitmq_url"])
queue = RabbitQueue(name=config["rabbitmq_queue"], durable=True)

LOG = get_logger()


@router.subscriber(queue)
async def create_order(
    model: OrderModel,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(ProcessOrderCommand(model=model))
