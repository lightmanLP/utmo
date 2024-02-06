from typing import Callable, TypeVar, Hashable, Generic, Mapping, TypeAlias, Literal, Any
from collections import defaultdict

from sortedcontainers import SortedList

KeyT = TypeVar("KeyT", bound=Hashable)
FuncT = TypeVar("FuncT", bound=Callable)
Events: TypeAlias = Literal[
    "core.init",
    "core.db.connect.sqlite",
]


class EventManager(Generic[KeyT]):
    handlers: Mapping[KeyT, SortedList[tuple[int, Callable]]]

    def __init__(self) -> None:
        self.handlers = defaultdict(lambda: SortedList(key=lambda x: x[0]))

    def on(self, key: KeyT, priority: int = 0) -> Callable[[FuncT], FuncT]:
        def decorator(func: FuncT) -> FuncT:
            self.add_handler(key, func, priority=priority)
            return func
        return decorator

    def add_handler(self, key: KeyT, func: FuncT, priority: int = 0):
        self.handlers[key].add((priority, func))

    def emit(self, key: KeyT, *args, **kwargs) -> tuple[Any, ...]:
        return tuple(f(*args, **kwargs) for _, f in self.handlers[key])

    def emitter(self, key: KeyT) -> Callable[..., tuple[Any, ...]]:
        def func(*args, **kwargs) -> tuple[Any, ...]:
            return self.emit(key, *args, **kwargs)
        return func


event_mngr = EventManager[Events]()
