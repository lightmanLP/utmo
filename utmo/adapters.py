from typing import Callable, Any
from abc import ABC, abstractmethod
from pathlib import Path
import webbrowser
import sys
import os

from . import structures


class AbstractSystemAdapter(ABC):
    """  """

    platform: structures.Platform
    vars_path: Path

    @property
    @abstractmethod
    def db_uri(self) -> str:
        ...

    @abstractmethod
    def open_url(self, url: str):
        ...


class AbstractControlAdapter(ABC):
    """  """

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
        if sys.platform in ("linux", "cygwin"):
            if "/com.termux/" in str(path):
                self.platform = structures.Platform.TERMUX
            else:
                self.platform = structures.Platform.LINUX
            self.vars_path = path.joinpath(".local", "lib", "utmo")
        elif "win" in sys.platform:
            self.platform = structures.Platform.WINDOWS
            self.vars_path = path.joinpath("Documents", "utmo")
        else:
            raise Exception("Unsupported platform")

    @property
    def db_uri(self) -> str:
        return f"sqlite:///{self.vars_path}/songs.db"

    def open_url(self, url: str):
        if self.platform == structures.Platform.TERMUX:
            os.system(f"termux-open-url {url}")
        else:
            webbrowser.open(url)


class ControlAdapter(AbstractControlAdapter):
    def get_input(
        self,
        text: str,
        input_type: Callable,
        secure: bool = False
    ) -> Any:
        return input_type(input())  # FIXME


system = SystemAdapter()
control = ControlAdapter()
