from typing import Any
from pathlib import Path
from enum import IntEnum, Enum

from typing_extensions import Self
import sqlalchemy as sqla


YDL_PARAMS: dict[str, Any] = {
    "format": "bestaudio/best",
    "quiet": True
}
LIBS_PATH: Path = Path(__package__) / "libs"


class Provider(IntEnum):
    LOCAL = 0
    REMOTE = 1
    YOUTUBE = 2
    BANDCAMP = 3
    VK = 4
    SOUNDCLOUD = 5
    GENERIC = 6


class Platform(IntEnum):
    WINDOWS = 0
    LINUX = 1
    TERMUX = 2
    MACOS = 3


class ControlMode(IntEnum):
    CLI = 0
    INTERACTIVE_TERM = 1
    TUI = 2


class Dialect(str, Enum):
    SQLITE = "sqlite"
    PG = "postgresql"

    @classmethod
    def from_engine(cls, engine: sqla.engine.Engine) -> Self:
        return cls(engine.dialect.name)

    def __str__(self) -> str:
        return self.value

    def __format__(self, format_spec: str) -> str:
        return str(self).__format__(format_spec)
