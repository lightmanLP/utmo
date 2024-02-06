from typing import Callable, Any
from abc import ABC, abstractmethod
from pathlib import Path
import functools
import webbrowser
import sys
import os

from .structures import ControlMode, Platform
from .exceptions import UnsupportedPlatformError


class AbstractSystemAdapter(ABC):
    """  """

    platform: Platform
    vars_path: Path
    config_path: Path
    default_db_uri: str
    default_builtin_sqlite: bool

    @abstractmethod
    def open_url(self, url: str):
        ...

    @abstractmethod
    def play_by_url(self, url: str, chooser: bool = False):
        ...


class AbstractControlAdapter(ABC):
    """  """

    mode: ControlMode | None = None

    @abstractmethod
    def get_input(
        self,
        text: str,
        input_type: Callable[[str], str] = str,
        secure: bool = False
    ) -> Any:
        ...


class SystemAdapter(AbstractSystemAdapter):
    def __init__(self) -> None:
        path = Path(os.path.expanduser("~"))
        platform = sys.platform.lower()

        if platform in ("linux", "linux2", "cygwin"):
            if "/com.termux/" in str(path):
                self.platform = Platform.TERMUX
            else:
                self.platform = Platform.LINUX
            self.vars_path = path / ".local" / "lib" / "utmo"
        elif "darwin" in platform:
            self.platform = Platform.MACOS
        elif "win" in platform:
            self.platform = Platform.WINDOWS
            self.vars_path = path / "AppData" / "Local" / "utmo"
        else:
            raise UnsupportedPlatformError(platform)

        self.vars_path = self.vars_path.resolve()
        self.vars_path.mkdir(parents=True, exist_ok=True)

        self.config_path = self.vars_path / "config.yml"
        self.config_path.touch(exist_ok=True)

    @functools.cached_property
    def default_builtin_sqlite(self) -> bool:
        return (self.platform == Platform.WINDOWS)

    @functools.cached_property
    def default_db_uri(self) -> str:
        prefix = "/" if (self.platform == Platform.LINUX) else ""
        return f"sqlite:///{prefix}{self.vars_path / 'songs.db'}"

    def open_url(self, url: str):
        if self.platform == Platform.TERMUX:
            os.system(f"termux-open-url '{url}'")
        else:
            webbrowser.open(url)

    def play_by_url(self, url: str, chooser: bool = False):
        if self.platform == Platform.TERMUX:
            os.system(
                f"termux-open "
                f"{'--chooser' if chooser else ''} "
                f"--content-type 'audio/mpeg' "
                f"'{url}'"
            )
        else:
            self.open_url(url)  # FIXME: запуск через плеер, проверка на локал


class ControlAdapter(AbstractControlAdapter):
    def get_input(
        self,
        text: str,
        input_type: Callable[[str], str] = str,
        secure: bool = False
    ) -> Any:
        return input_type(input(text))  # FIXME


system = SystemAdapter()
control = ControlAdapter()
