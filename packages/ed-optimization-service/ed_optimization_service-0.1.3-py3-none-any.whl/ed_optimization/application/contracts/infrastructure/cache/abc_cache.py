from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ABCCache(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: str) -> T | None: ...

    @abstractmethod
    def set(self, key: str, value: T) -> None: ...
