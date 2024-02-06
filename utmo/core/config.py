from typing import TypeVar, Annotated, TypeAlias, overload
from pathlib import Path
import io

from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, AfterValidator, Field
import oyaml as yaml

from . import adapters
from .structures import Platform

T = TypeVar("T")


def yaml_multiline_str_repr(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data,
        style=("|" if ("\n" in data) else None)
    )


yaml.add_representer(str, yaml_multiline_str_repr)


def windows_feat(val: bool) -> bool:
    if val:
        assert adapters.system.platform == Platform.WINDOWS, "windows-only feature"


WindowsFeat: TypeAlias = AfterValidator(windows_feat)


class Model(BaseModel):
    __abstract__ = True

    model_config = ConfigDict(extra="forbid", frozen=True)


class DB(Model):
    uri: str = adapters.system.default_db_uri
    use_builtin_sqlite: Annotated[bool, WindowsFeat] = adapters.system.default_builtin_sqlite


class Debug(Model):
    enabled: bool = False


class Config(Model):
    db: DB = Field(default_factory=DB)
    debug: Debug = Field(default_factory=Debug)

    def write_config(self, path: Path):
        with open(path, "w", encoding="UTF-8") as file:
            yaml.dump(self.model_dump(), file)

    @classmethod
    def from_dump(cls, dump: dict | Path | str) -> Self:
        assert isinstance(dump, (dict, str, Path))
        data = cls.read_dump(dump)
        instance = cls(**data)

        if isinstance(dump, Path) and not data:
            instance.write_config(dump)
        return instance

    @overload
    @staticmethod
    def read_dump(dump: str | Path) -> dict:
        ...

    @overload
    @staticmethod
    def read_dump(dump: T) -> T:
        ...

    @staticmethod
    def read_dump(dump: T) -> dict | T:
        match dump:
            case Path():
                assert dump.exists() and dump.is_file()
                with open(dump, "r", encoding="UTF-8") as file:
                    return yaml.load(file, yaml.FullLoader) or dict()
            case str():
                return yaml.load(io.StringIO(dump), yaml.FullLoader) or dict()
            case _:
                return dump


config = Config.from_dump(adapters.system.config_path)
