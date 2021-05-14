from typing import Any, Optional
from abc import ABC, abstractmethod


class AbstractExtractor(ABC):
    """ Extract audio stream """

    url: str
    loc_data: Any

    @abstractmethod
    def extract(self) -> Optional[str]:
        """  """
        ...
