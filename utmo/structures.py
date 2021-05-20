from typing import Tuple
from dataclasses import dataclass
from enum import IntEnum


@dataclass
class VKSong:
    id: int
    owner_id: int


class Providers(IntEnum):
    LOCAL = 0
    YOUTUBE = 1
    BANDCAMP = 2
    VK = 3
    SOUNDCLOUD = 4
    CUSTOM = 5


class Platform(IntEnum):
    WINDOWS = 0
    LINUX = 1
    TERMUX = 2


YDL_PARAMS = {
    "format": "bestaudio/best"
}
