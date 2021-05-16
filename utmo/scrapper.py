from typing import List
from abc import ABC, abstractmethod
from datetime import datetime
import re

import youtube_dl
from vk_api.audio import VkAudio

from . import models, enums, const, dataclasses


class AbstractScrapper(ABC):
    """  """

    @abstractmethod
    def scrap(self, url: str, provider: enums.Providers) -> List[models.Song]:
        """  """
        ...


class Scrapper(AbstractScrapper):
    vk_audio_pattern: re.Pattern = re.compile(r"audio(\d+)_(\d+)")
    vk_playlist_pattern: re.Pattern = re.compile(r"audio_playlist(\d+)_(\d+)/(\w+)")
    vk: VkAudio

    def __init__(self, vk: VkAudio) -> None:
        self.vk = vk

    def scrap(self, url: str, provider: enums.Providers) -> List[models.Song]:
        if provider == enums.Providers.VK:
            return self._from_vk(url)
        elif provider == enums.Providers.CUSTOM:
            return self._from_custom(url)
        else:
            with youtube_dl.YoutubeDL(const.YDL_PARAMS) as ydl:
                data = ydl.extract_info(url, download=False)
            if "entries" in data:
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

    def _from_vk(self, url: str) -> List[models.Song]:
        peers = self.vk_audio_pattern.search(url)
        if peers:
            data = self.vk.get_audio_by_id(*peers.groups()[1:])
            return [
                models.Song(
                    url="",
                    title=data["title"],
                    author=data["artist"],
                    description=data.get("description", ""),
                    provided_from=enums.Providers.VK,
                    tags=set(),
                    import_date=datetime.now(),
                    extra_location_data=dataclasses.VKSong(
                        peers[2],
                        peers[1]
                    )
                )
            ]
        else:
            peers = self.vk_playlist_pattern.search(url)
            self.vk.get(*peers.groups()[1:])  # FIXME: ну не работает оно блять
            return None

    def _from_custom(self, url: str) -> List[models.Song]:
        ...  # TODO
