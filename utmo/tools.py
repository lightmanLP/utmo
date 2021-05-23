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

    vk_pattern: re.Pattern
    vk_audio_pattern: re.Pattern
    vk_playlist_pattern: re.Pattern

    @classmethod
    @abstractmethod
    def scrap(cls, url: str) -> List[models.Song]:
        """  """
        ...


class AbstractExtractor(ABC):
    """ Extract audio stream """

    @classmethod
    @abstractmethod
    def extract(cls, song: models.Song) -> Optional[str]:
        """  """
        ...


class Scrapper(AbstractScrapper):  # FIXME
    """ Scrap track data """

    vk_pattern = re.compile(r"https://(?:www.)?vk.com/")
    vk_audio_pattern = re.compile(r"audio(\d+)_(\d+)")
    vk_playlist_pattern = re.compile(r"(?:audio_playlist|playlist/)(\d+)_(\d+)(?:/(\w+))?")

    @classmethod
    def scrap(cls, url: str) -> List[models.Song]:
        if cls.vk_pattern.search(url) is not None:
            songs = cls._from_vk(url)
        else:
            with youtube_dl.YoutubeDL(structures.YDL_PARAMS) as ydl:
                data = ydl.extract_info(url, download=False)
            provider = None
            for i in structures.Providers:
                if i.name.lower() in data["extractor"].lower():
                    provider = i
                    break

            if provider is None:
                songs = cls._from_custom(data)
            else:
                if "entries" in data:
                    tracks = data["entries"]
                else:
                    tracks = [data]
                songs = list()
                for i in tracks:
                    song = models.Song(
                        url=i["webpage_url"],
                        title=i.get("track", i["title"]),
                        author=i.get("artist", i["uploader"]),
                        description=i.get("description", ""),
                        provider=provider,
                        import_date=datetime.now()
                    )
                    song.tags.extend(
                        [
                            models.Tag(tag=i.lower())
                            for i in set(i.get("tags", tuple()))
                        ]
                    )
                    songs.append(song)
                    models.session.merge(song)
        models.session.commit()
        return songs

    @classmethod
    def _from_vk(cls, url: str) -> List[models.Song]:
        peers = cls.vk_audio_pattern.search(url)
        if peers:
            data = [vk_manager.vk.get_audio_by_id(*peers.groups())]
        else:
            peers = cls.vk_playlist_pattern.search(url)
            data = vk_manager.vk.get(*peers.groups())
        songs = [
            models.Song(
                url="",
                title=i["title"],
                author=i["artist"],
                description=i.get("description", ""),
                provider=structures.Providers.VK,
                import_date=datetime.now(),
                extra_location_data=structures.VKSong(
                    i["id"],
                    i["owner_id"]
                )
            )
            for i in data
        ]
        models.session.add_all(songs)
        return songs

    def _from_custom(ydl_data: dict) -> List[models.Song]:
        ...  # TODO


class Extractor(AbstractExtractor):
    """ Extract audio stream """

    @classmethod
    def extract(cls, song: models.Song) -> Optional[str]:
        if song.provider == structures.Providers.VK:
            return cls._from_vk(song.extra_location_data)
        elif song.provider == structures.Providers.CUSTOM:
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
