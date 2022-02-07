from typing import Optional
from pathlib import Path

import yaml


from . import adapters, structures
from .exceptions import ConfigParseError


class Config:
    db_uri: str
    use_builtin_sqlite: bool

    def __init__(
        self,
        db_uri: Optional[str] = None,
        use_builtin_sqlite: Optional[bool] = None
    ) -> None:
        if db_uri is None:
            db_uri = adapters.system.default_db_uri
        if use_builtin_sqlite is None:
            use_builtin_sqlite = adapters.system.default_builtin_sqlite
        loc = locals().copy()
        del loc["self"]
        self.__dict__.update(loc)
        self.validate()

    def validate(self):
        if self.use_builtin_sqlite:
            assert adapters.system.platform == structures.Platform.WINDOWS

    @classmethod
    def from_path(cls, path: Path) -> "Config":
        data = yaml.load(path.read_text("utf-8"), yaml.FullLoader)
        if data is None:
            data = dict()
        if not isinstance(data, dict):
            raise ConfigParseError()
        return cls(**data)


config = Config.from_path(adapters.system.config_path)
