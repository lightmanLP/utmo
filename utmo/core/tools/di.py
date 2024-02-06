from typing import TypeVar, Generic, ClassVar, Any

from .exceptions import InjectionError

T = TypeVar("T")


class DI(Generic[T]):
    container: ClassVar[dict[str | type, Any]] = dict()
    key: str | type[T]

    def __init__(self, key: str | type[T]) -> None:
        self.key = key

    def __get__(self) -> T:
        return self.get(self.key)

    @classmethod
    def store(cls, value: T, key: str | type[T] | None = None) -> T:
        if key is None:
            key = type(value)
        cls.container[key] = value

    @classmethod
    def get(cls, key: str | type[T]) -> T:
        value = cls.container.get(key)
        if value is None:
            raise InjectionError(key)
        return value
