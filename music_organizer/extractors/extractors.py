from typing import Optional

from vk_api.audio import VkAudio

from .abc import AbstractExtractor
from .. import dataclasses


class YoutubeExtractor(AbstractExtractor):
    ...


class BandcampExtractor(AbstractExtractor):
    ...


class VKExtractor(AbstractExtractor):
    loc_data: dataclasses.VkSong
    vk: VkAudio

    def __init__(
        self,
        url: str,
        loc_data: int,
        vk: VkAudio
    ) -> None:
        self.url = url
        self.loc_data = loc_data
        self.vk = vk

    def extract(self) -> Optional[str]:
        audio = self.vk.get_audio_by_id(
            self.loc_data.owner_id,
            self.loc_data.id
        )
        return audio.get("url")


class SpotifyExtractor(AbstractExtractor):
    ...


class SoundCloudExtractor(AbstractExtractor):
    ...


class CustomExtractor(AbstractExtractor):
    ...
