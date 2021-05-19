from typing import List, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import re

from urllib3.util import parse_url
import youtube_dl

from . import models, structures
from .dynamic_storage import vk_manager


class AbstractScrapper(ABC):
    """ Scrap track data """

    vk_audio_pattern: re.Pattern
    vk_playlist_pattern: re.Pattern

    @classmethod
    @abstractmethod
    def scrap(cls, url: str, provider: structures.Providers) -> List[models.Song]:
        """  """
        ...

    @abstractmethod
    def detect_provider(url: str) -> structures.Providers:
        """  """
        ...


class AbstractExtractor(ABC):
    """ Extract audio stream """

    @classmethod
    @abstractmethod
    def extract(cls, song: models.Song) -> Optional[str]:
        """  """
        ...


class Scrapper(AbstractScrapper):
    """ Scrap track data """

    vk_audio_pattern = re.compile(r"audio(\d+)_(\d+)")
    vk_playlist_pattern = re.compile(r"audio_playlist(\d+)_(\d+)(?:/(\w+))?")

    @classmethod
    def scrap(cls, url: str, provider: structures.Providers) -> List[models.Song]:
        if provider is None:
            provider = cls.detect_provider(url)

        if provider == structures.Providers.VK:
            return cls._from_vk(url)
        elif provider == structures.Providers.CUSTOM:
            return cls._from_custom(url)
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

    def detect_provider(url: str) -> structures.Providers:
        url_ = parse_url(url)
        if url_.hostname.endswith("vk.com"):
            return structures.Providers.VK
        elif url_.hostname.endswith("youtube.com"):
            return structures.Providers.YOUTUBE
        elif url_.hostname.endswith("soundcloud.com"):
            return structures.Providers.SOUNDCLOUD
        ...  # TODO

    @classmethod
    def _from_vk(cls, url: str) -> List[models.Song]:
        peers = cls.vk_audio_pattern.search(url)
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
            peers = cls.vk_playlist_pattern.search(url)
            vk_manager.vk.get(*peers.groups()[1:])  # FIXME: ну не работает оно блять
            return None

    def _from_custom(url: str) -> List[models.Song]:
        ...  # TODO


class Extractor(AbstractExtractor):
    """ Extract audio stream """

    @classmethod
    def extract(cls, song: models.Song) -> Optional[str]:
        if song.provided_from == structures.Providers.VK:
            return cls._from_vk(song.extra_location_data)
        elif song.provided_from == structures.Providers.CUSTOM:
            return cls._from_custom(song)  # FIXME
        else:
            return cls._from_yt(song.url)

    def _from_yt(url: str) -> Optional[str]:
        with youtube_dl.YoutubeDL(structures.YDL_PARAMS) as ydl:
            info = ydl.extract_info(url, download=False)
        return info.get("url")

    def _from_vk(loc_data: structures.VKSong) -> Optional[str]:
        audio = vk_manager.vk.get_audio_by_id(
            loc_data.owner_id,
            loc_data.id
        )
        return audio.get("url")

    def _from_custom(song: models.Song) -> Optional[str]:
        ...  # TODO
