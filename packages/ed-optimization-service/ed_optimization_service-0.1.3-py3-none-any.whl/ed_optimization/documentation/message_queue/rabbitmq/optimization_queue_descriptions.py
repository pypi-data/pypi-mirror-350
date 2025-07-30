from ed_domain.documentation.message_queue.rabbitmq.abc_queue_descriptions import \
    ABCQueueDescriptions
from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription

from ed_optimization.application.features.order.dtos import CreateOrderDto


class OptimizationQueueDescriptions(ABCQueueDescriptions):
    def __init__(self, connection_url: str) -> None:
        self._descriptions: list[QueueDescription] = [
            {
                "name": "create_order",
                "connection_parameters": {
                    "url": connection_url,
                    "queue": "create_order",
                },
                "durable": True,
                "request_model": CreateOrderDto,
            },
        ]

    @property
    def descriptions(self) -> list[QueueDescription]:
        return self._descriptions
