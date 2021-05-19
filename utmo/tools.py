from typing import List, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import re

import youtube_dl
from vk_api.audio import VkAudio

from . import models, structures
from .dynamic_storage import vk_manager


class AbstractScrapper(ABC):
    """ Scrap track data """

    vk_audio_pattern: re.Pattern
    vk_playlist_pattern: re.Pattern

    @abstractmethod
    def scrap(self, url: str, provider: structures.Providers) -> List[models.Song]:
        """  """
        ...


class AbstractExtractor(ABC):
    """ Extract audio stream """

    @abstractmethod
    def extract(self, song: models.Song) -> Optional[str]:
        """  """
        ...


class Scrapper(AbstractScrapper):
    vk_audio_pattern = re.compile(r"audio(\d+)_(\d+)")
    vk_playlist_pattern = re.compile(r"audio_playlist(\d+)_(\d+)/(\w+)")

    def scrap(self, url: str, provider: structures.Providers) -> List[models.Song]:
        if provider == structures.Providers.VK:
            return self._from_vk(url)
        elif provider == structures.Providers.CUSTOM:
            return self._from_custom(url)
        else:
            with youtube_dl.YoutubeDL(structures.YDL_PARAMS) as ydl:
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
            data = vk_manager.vk.get_audio_by_id(*peers.groups()[1:])
            return [
                models.Song(
                    url="",
                    title=data["title"],
                    author=data["artist"],
                    description=data.get("description", ""),
                    provided_from=structures.Providers.VK,
                    tags=set(),
                    import_date=datetime.now(),
                    extra_location_data=structures.VKSong(
                        peers[2],
                        peers[1]
                    )
                )
            ]
        else:
            peers = self.vk_playlist_pattern.search(url)
            vk_manager.vk.get(*peers.groups()[1:])  # FIXME: ну не работает оно блять
            return None

    def _from_custom(self, url: str) -> List[models.Song]:
        ...  # TODO


class Extractor(AbstractExtractor):
    @property
    def vk(self) -> VkAudio:
        ...  # TODO

    def extract(self, song: models.Song) -> Optional[str]:
        if song.provided_from == structures.Providers.VK:
            return self._from_vk(song.extra_location_data)
        elif song.provided_from == structures.Providers.CUSTOM:
            return self._from_custom(song)  # FIXME
        else:
            return self._from_yt(song.url)

    def _from_yt(self, url: str) -> Optional[str]:
        with youtube_dl.YoutubeDL(structures.YDL_PARAMS) as ydl:
            info = ydl.extract_info(url, download=False)
        return info.get("url")

    def _from_vk(self, loc_data: structures.VKSong) -> Optional[str]:
        audio = self.vk.get_audio_by_id(
            loc_data.owner_id,
            loc_data.id
        )
        return audio.get("url")

    def _from_custom(self, song: models.Song) -> Optional[str]:
        ...  # TODO
