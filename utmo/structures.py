from typing import Dict, Any, Set
from dataclasses import dataclass
from enum import Enum, IntEnum
from pathlib import Path


YDL_PARAMS: Dict[str, Any] = {
    "format": "bestaudio/best",
    "quiet": True
}
NONEXPORTED_PARAMS: Set[str] = {
    "id",
    "import_date",
    "_sa_instance_state"
}
SQLITE_EXTENSIONS_PATH: Path = Path(__package__) / "sqlite_ext"


@dataclass
class VKSong:
    id: int
    owner_id: int


class Provider(IntEnum):
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
    MACOS = 3


class ControlMode(IntEnum):
    CLI = 0
    INTERACTIVE_TERM = 1
    TUI = 2


class Dialect(Enum):
    SQLITE = "sqlite"
    PG = "postgresql"
