from typing import List
from abc import ABC, abstractmethod

from .. import models


class AbstractScrapper(ABC):
    """  """

    @abstractmethod
    def scrap(self, url: str) -> models.Song:
        """  """
        ...

    @abstractmethod
    def scrap_multiple(self, url: str) -> List[models.Song]:
        """  """
        ...
