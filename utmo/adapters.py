from typing import Callable, Any
from abc import ABC, abstractmethod


class AbstractSystemAdapter(ABC):
    """  """
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
