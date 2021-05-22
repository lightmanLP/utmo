from typing import Set
from dataclasses import dataclass
from enum import IntEnum


YDL_PARAMS: dict = {
    "format": "bestaudio/best",
    "quiet": True
}
NONEXPORTED_PARAMS: Set[str] = {
    "id",
    "import_date",
    "_sa_instance_state"
}


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


class ControlMode(IntEnum):
    CLI = 0
    INTERACTIVE_TERM = 1
