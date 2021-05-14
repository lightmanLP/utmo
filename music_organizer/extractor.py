from typing import Optional
from abc import ABC, abstractmethod

from vk_api.audio import VkAudio
import youtube_dl

from . import models, dataclasses, const, enums


class AbstractExtractor(ABC):
    """ Extract audio stream """

    @abstractmethod
    def extract(self, song: models.Song) -> Optional[str]:
        """  """
        ...


class Extractor(AbstractExtractor):
    vk: VkAudio

    def __init__(self, vk: VkAudio) -> None:
        self.vk = vk

    def extract(self, song: models.Song) -> Optional[str]:
        if song.provided_from == enums.Providers.VK:
            return self._from_vk(song.extra_location_data)
        elif song.provided_from == enums.Providers.CUSTOM:
            return self._from_custom(song)  # FIXME
        else:
            return self._from_yt(song.url)

    def _from_yt(self, url: str) -> Optional[str]:
        with youtube_dl.YoutubeDL(const.YDL_PARAMS) as ydl:
            info = ydl.extract_info(url, download=False)
        return info.get("url")

    def _from_vk(self, loc_data: dataclasses.VKSong) -> Optional[str]:
        audio = self.vk.get_audio_by_id(
            loc_data.owner_id,
            loc_data.id
        )
        return audio.get("url")

    def _from_custom(self, song: models.Song) -> Optional[str]:
        ...  # TODO
