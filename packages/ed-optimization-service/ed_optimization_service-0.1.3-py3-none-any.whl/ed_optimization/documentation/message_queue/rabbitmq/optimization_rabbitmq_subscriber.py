from ed_infrastructure.documentation.message_queue.rabbitmq.rabbitmq_producer import \
    RabbitMQProducer

from ed_optimization.application.features.order.dtos.create_order_dto import \
    CreateOrderDto
from ed_optimization.documentation.message_queue.rabbitmq.abc_optimization_rabbitmq_subscriber import \
    ABCOptimizationRabbitMQSubscriber
from ed_optimization.documentation.message_queue.rabbitmq.optimization_queue_descriptions import \
    OptimizationQueueDescriptions


class OptimizationRabbitMQSubscriber(ABCOptimizationRabbitMQSubscriber):
    def __init__(self, connection_url: str) -> None:
        self._connection_url = connection_url
        self._queues = OptimizationQueueDescriptions(connection_url)

    def create_order(self, create_order_dto: CreateOrderDto) -> None:
        queue = self._queues.get_queue("create_delivery_job")
        producer = RabbitMQProducer[CreateOrderDto](
            queue["connection_parameters"]["url"],
            queue["connection_parameters"]["queue"],
        )
        producer.start()
        producer.publish(create_order_dto)
        producer.stop()
