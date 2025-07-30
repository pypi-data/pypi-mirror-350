from abc import ABCMeta, abstractmethod

from ed_optimization.application.features.order.dtos.create_order_dto import \
    CreateOrderDto


class ABCOptimizationRabbitMQSubscriber(metaclass=ABCMeta):
    @abstractmethod
    def create_order(self, create_order_dto: CreateOrderDto) -> None: ...
