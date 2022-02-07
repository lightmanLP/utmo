from typing import Callable, Optional, Any
from abc import ABC, abstractmethod
from pathlib import Path
import webbrowser
import sys
import os

from . import structures
from .exceptions import UnsupportedPlatformError


class AbstractSystemAdapter(ABC):
    """  """

    platform: structures.Platform
    vars_path: Path
    config_path: Path

    @property
    @abstractmethod
    def default_db_uri(self) -> str:
        ...

    @abstractmethod
    def open_url(self, url: str):
        ...

    @abstractmethod
    def play_by_url(self, url: str, chooser: bool = False):
        ...


class AbstractControlAdapter(ABC):
    """  """

    mode: Optional[structures.ControlMode] = None

    @abstractmethod
    def get_input(
        self,
        text: str,
        input_type: Callable = str,
        secure: bool = False
    ) -> Any:
        ...


class SystemAdapter(AbstractSystemAdapter):
    def __init__(self) -> None:
        path = Path(os.path.expanduser("~"))
        platform = sys.platform.lower()
        if platform in ("linux", "linux2", "cygwin"):
            if "/com.termux/" in str(path):
                self.platform = structures.Platform.TERMUX
            else:
                self.platform = structures.Platform.LINUX
            self.vars_path = path / ".local" / "lib" / "utmo"
        elif "darwin" in platform:
            self.platform = structures.Platform.MACOS
        elif "win" in platform:
            self.platform = structures.Platform.WINDOWS
            self.vars_path = path / "AppData" / "Local" / "utmo"
        else:
            raise UnsupportedPlatformError(platform)

        self.vars_path = self.vars_path.resolve()
        self.vars_path.mkdir(parents=True, exist_ok=True)
        self.config_path = self.vars_path / "config.yml"
        self.config_path.touch(exist_ok=True)

    @property
    def default_db_uri(self) -> str:
        prefix = "/" if self.platform == structures.Platform.LINUX else ""
        return f"sqlite:///{prefix}{self.vars_path / 'songs.db'}"

    def open_url(self, url: str):
        if self.platform == structures.Platform.TERMUX:
            os.system(f"termux-open-url '{url}'")
        else:
            webbrowser.open(url)

    def play_by_url(self, url: str, chooser: bool = False):
        if self.platform == structures.Platform.TERMUX:
            os.system(
                f"termux-open {'--chooser' if chooser else ''} --content-type 'audio/mpeg' '{url}'"
            )
        else:
            self.open_url(url)  # FIXME: запуск через плеер, проверка на локал


class ControlAdapter(AbstractControlAdapter):
    def get_input(
        self,
        text: str,
        input_type: Callable = str,
        secure: bool = False
    ) -> Any:
        return input_type(input(text))  # FIXME


system = SystemAdapter()
control = ControlAdapter()
