from typing import Optional
from pathlib import Path

import yaml


from . import adapters
from .exceptions import ConfigParseError


class Config:
    db_uri: str

    def __init__(self, db_uri: Optional[str] = None) -> None:
        if db_uri is None:
            db_uri = adapters.system.default_db_uri
        self.db_uri = db_uri

    @classmethod
    def from_path(cls, path: Path) -> "Config":
        data = yaml.load(path.read_text("utf-8"), yaml.FullLoader)
        if data is None:
            data = dict()
        if not isinstance(data, dict):
            raise ConfigParseError()
        return cls(**data)
