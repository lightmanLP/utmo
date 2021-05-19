from typing import Callable, Any
from abc import ABC, abstractmethod


class AbstractSystemAdapter(ABC):
    """  """

    @abstractmethod
    def open_url(url: str):
        ...


class AbstractControlAdapter(ABC):
    """  """

    @abstractmethod
    def get_input(
        self,
        text: str,
        input_type: Callable = str
    ) -> Any:
        ...


class SystemAdapter(AbstractSystemAdapter):
    ...


class ControlAdapter(AbstractControlAdapter):
    ...


system = SystemAdapter()
control = ControlAdapter()
