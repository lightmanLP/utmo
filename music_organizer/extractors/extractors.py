from typing import Optional

from vk_api.audio import VkAudio
import youtube_dl

from .abc import AbstractExtractor
from .. import dataclasses
from .. import const


class YoutubeExtractor(AbstractExtractor):
    def extract(self, url: str) -> Optional[str]:
        with youtube_dl.YoutubeDL(const.YDL_PARAMS) as ydl:
            info = ydl.extract_info(url, download=False)
        return info.get("url")


class VKExtractor(AbstractExtractor):
    vk: VkAudio

    def __init__(self, vk: VkAudio) -> None:
        self.vk = vk

    def extract(self, loc_data: dataclasses.VKSong) -> Optional[str]:
        audio = self.vk.get_audio_by_id(
            loc_data.owner_id,
            loc_data.id
        )
        return audio.get("url")


class SpotifyExtractor(AbstractExtractor):
    ...


class CustomExtractor(AbstractExtractor):
    ...


BandcampExtractor = SoundCloudExtractor = YoutubeExtractor
