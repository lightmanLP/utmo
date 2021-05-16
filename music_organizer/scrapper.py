from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

import youtube_dl

from . import models, enums, const


class AbstractScrapper(ABC):
    """  """

    @abstractmethod
    def scrap(
        self,
        url: str,
        provider: enums.Providers,
        multiple: bool = False
    ) -> List[models.Song]:
        """  """
        ...


class Scrapper(AbstractScrapper):
    def scrap(
        self,
        url: str,
        provider: enums.Providers,
        multiple: bool = False
    ) -> List[models.Song]:
        if provider == enums.Providers.VK:
            self._from_vk(url)
        elif provider == enums.Providers.CUSTOM:
            self._from_custom(url)
        else:
            with youtube_dl.YoutubeDL(const.YDL_PARAMS) as ydl:
                data = ydl.extract_info(url, download=False)
            if multiple:
                tracks = data["entries"]
            else:
                tracks = [data]
            return [
                models.Song(
                    url=i["webpage_url"],
                    title=i.get("track", i["title"]),
                    author=i.get("artist", i["uploader"]),
                    description=i.get("description", ""),
                    provided_from=provider,
                    tags=set(i.get("tags", tuple())),
                    import_date=datetime.now()
                )
                for i in tracks
            ]
