from typing import TypeVar

from ed_domain.queues.ed_optimization.order_model import OrderModel

from ed_optimization.application.contracts.infrastructure.cache.abc_cache import \
    ABCCache

T = TypeVar("T")


class InMemoryCache(ABCCache[list[OrderModel]]):
    def __init__(self) -> None:
        self._cache: dict[str, list[OrderModel]] = {}

    def get(self, key: str) -> list[OrderModel] | None:
        return self._cache.get(key)

    def set(self, key: str, value: list[OrderModel]) -> None:
        self._cache[key] = value
