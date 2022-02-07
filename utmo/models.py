from __future__ import annotations
from typing import TYPE_CHECKING, Generic, TypeVar, Optional, Union, List, Any
from pathlib import Path
from enum import Enum, IntEnum
from datetime import datetime
import functools

import sqlalchemy as sqla
from sqlalchemy import event
from sqlalchemy.sql import functions
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from alembic import command, config

from . import adapters, structures
from .exceptions import UnsupportedDBDialectError

if TYPE_CHECKING:
    import sqlite3

T = TypeVar("T", bound=IntEnum)

Base = declarative_base()
Column = functools.partial(sqla.Column, nullable=False)  # type: sqla.Column


class IntEnumType(sqla.TypeDecorator, Generic[T]):
    impl = sqla.Integer
    enumtype: type[T]

    def __init__(self, enumtype: type[T], *args, **kwargs) -> None:
        self.enumtype = enumtype
        super().__init__(*args, **kwargs)

    def process_bind_param(
        self,
        value: Union[int, T],
        dialect: sqla.sql.type_api.Dialect
    ) -> Optional[int]:
        if isinstance(value, self.enumtype):
            return value.value
        return value

    def process_result_value(
        self,
        value: Union[int, Enum],
        dialect: Any
    ) -> Optional[Enum]:
        if value is None:
            return None
        elif isinstance(value, self.stored_enum):
            return value
        return self.stored_enum(value)

    def coerce_compared_value(self, op: Any, value: Any) -> Any:
        if value is None:
            return None
        elif isinstance(value, int):
            return sqla.Integer()
        else:
            return self


class PathType(sqla.TypeDecorator):
    impl = sqla.Text

    def process_bind_param(
        self,
        value: Any,
        dialect: Any
    ) -> Optional[str]:
        if value is None:
            return ""
        elif isinstance(value, str):
            return value
        return str(value)

    def process_result_value(
        self,
        value: Any,
        dialect: Any
    ) -> Optional[int]:
        if value is None or value == "":
            return None
        elif isinstance(value, int):
            return value
        return int(value)

    def coerce_compared_value(self, op: Any, value: Any) -> Any:
        if value is None:
            return None
        return self


def edit_distance(*args, **kwargs) -> functions.Function:
    if engine.dialect.name == structures.Dialect.SQLITE:
        return functions.func.editdist3(*args, **kwargs)


songs_to_tags = sqla.Table(
    "songs_to_tags",
    Base.metadata,
    Column("song_id", sqla.Integer, sqla.ForeignKey("songs.id"), primary_key=True),
    Column("tag", sqla.Integer, sqla.ForeignKey("tags.tag"), primary_key=True)
)


class Song(Base):
    __tablename__ = "songs"

    id: int = Column(sqla.Integer, primary_key=True, autoincrement=True)
    url: Optional[str] = Column(sqla.Text, nullable=True, default=None)
    file_path: Optional[Path] = Column()
    title = Column(sqla.UnicodeText)
    author = Column(sqla.UnicodeText)
    description = Column(sqla.UnicodeText, default="")
    provider = Column(sqla.Integer)
    plays_count = Column(sqla.Integer, default=0)
    import_date = Column(sqla.DateTime, default=datetime.now)
    extra_location_data = Column(sqla.PickleType, nullable=True, default=None)

    tags = relationship("Tag", secondary=songs_to_tags, back_populates="songs")

    def __repr__(self) -> str:
        return f"{self.title} {chr(8212)} {self.author}"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Song):
            return self.id == o.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def export_songs(
        cls,
        with_plays: bool = False,
        with_locals: bool = False
    ) -> List[dict]:
        query = session.query(cls)
        if not with_locals:
            query.filter(cls.provider != structures.Provider.LOCAL)
        songs = query.all()
        if not songs:
            return list()

        attrs = set(songs[0].__dict__).difference(structures.NONEXPORTED_PARAMS)
        if not with_plays:
            attrs.remove("plays_count")
        return [
            {
                i: getattr(song, i)
                for i in attrs
            }
            for song in songs
        ]

    @classmethod
    def import_songs(cls, data: List[dict]):
        songs = [
            cls(**i)
            for i in data
        ]
        session.add_all(songs)
        session.commit()


class Tag(Base):
    __tablename__ = "tags"

    tag = Column(sqla.UnicodeText, primary_key=True)
    category = Column(sqla.Enum)  # TODO

    songs = relationship("Song", secondary=songs_to_tags, back_populates="tags")

    def __repr__(self) -> str:
        return self.tag


def load_extensions(dbapi_connection: sqlite3.Connection, connection_record):
    dbapi_connection.enable_load_extension(True)
    for i in structures.SQLITE_EXTENSIONS_PATH.iterdir():
        dbapi_connection.load_extension(str(i))
    dbapi_connection.enable_load_extension(False)


def init():
    global engine, Session, session

    engine = sqla.create_engine(adapters.system.db_uri, echo=False)
    if engine.dialect.name not in structures.Dialect:
        raise UnsupportedDBDialectError(engine.dialect.name)
    elif engine.dialect.name == structures.Dialect.SQLITE:
        event.listen(engine, "connect", load_extensions)
    al_cfg = config.Config()
    al_cfg.set_main_option("script_location", "utmo:alembic")
    al_cfg.set_main_option("sqlalchemy.url", adapters.system.db_uri)
    command.upgrade(al_cfg, "head")

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
