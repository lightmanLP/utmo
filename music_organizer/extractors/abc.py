from typing import Optional
from abc import ABC, abstractmethod


class AbstractExtractor(ABC):
    """ Extract audio stream """

    @abstractmethod
    def extract(self) -> Optional[str]:
        """  """
        ...
