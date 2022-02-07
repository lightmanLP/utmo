from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, Set
from dataclasses import dataclass
from enum import Enum, IntEnum
from pathlib import Path

import sqlalchemy as sqla

if TYPE_CHECKING:
    from typing_extensions import Self


YDL_PARAMS: Dict[str, Any] = {
    "format": "bestaudio/best",
    "quiet": True
}
NONEXPORTED_PARAMS: Set[str] = {
    "id",
    "import_date",
    "_sa_instance_state"
}
LIBS_PATH: Path = Path(__package__) / "libs"


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

    @classmethod
    def from_engine(cls, engine: sqla.engine.Engine) -> Self:
        return cls(engine.dialect.name)
