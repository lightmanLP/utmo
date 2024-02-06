import functools
from datetime import datetime

from sqlalchemy import event as sqla_event
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    sessionmaker,
    mapped_column as _mapped_column,
    relationship,
)
import sqlalchemy as sqla
from alembic import command as alembic_cmd
from alembic.config import Config as AlConfig

from ..structures import Dialect, Provider
from ..config import config
from ..tools import event_mngr, DI
from ..exceptions import UnsupportedDBDialectError
from .fields import IntEnumType

engine: sqla.Engine | None = None
Session: sessionmaker = None
mapped_column = functools.partial(_mapped_column, nullable=False)


class Base(DeclarativeBase):
    ...


songs_to_tags = sqla.Table(
    "songs_to_tags",
    Base.metadata,
    sqla.Column("song_id", sqla.Integer, sqla.ForeignKey("songs.id"), primary_key=True),
    sqla.Column("tag", sqla.Integer, sqla.ForeignKey("tags.tag"), primary_key=True)
)


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sqla.UnicodeText)
    author: Mapped[str] = mapped_column(sqla.UnicodeText)
    description: Mapped[str] = mapped_column(sqla.UnicodeText, default="")

    provider: Mapped[Provider] = mapped_column(IntEnumType(Provider))

    plays_count: Mapped[int] = mapped_column(sqla.Integer, default=0)
    import_date: Mapped[datetime] = mapped_column(sqla.DateTime, default=datetime.now)

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=songs_to_tags,
        back_populates="songs"
    )

    def __str__(self) -> str:
        return f"{self.title} {chr(8212)} {self.author}"

    def __format__(self, format_spec: str) -> str:
        return str(self).__format__(format_spec)

    def __eq__(self, obj: object) -> bool:
        match obj:
            case Song():
                return self.id == obj.id
            case int():
                return self.id == obj
            case _:
                return False

    def __hash__(self) -> int:
        return self.id


class Tag(Base):
    __tablename__ = "tags"

    tag: Mapped[str] = mapped_column(sqla.UnicodeText, primary_key=True)
    category: Mapped[str] = mapped_column(sqla.Enum)

    songs: Mapped[list["Song"]] = relationship(
        "Song",
        secondary=songs_to_tags,
        back_populates="tags"
    )

    def __str__(self) -> str:
        return self.tag

    def __format__(self, format_spec: str) -> str:
        return str(self).__format__(format_spec)


@event_mngr.on("core.init")
def init():
    global engine, Session

    engine = DI.store(
        sqla.create_engine(
            config.db.uri,
            echo=config.debug.enabled
        )
    )
    try:
        dialect = DI.store(Dialect.from_engine(engine))
    except ValueError:
        raise UnsupportedDBDialectError(engine.dialect.name)
    if dialect == Dialect.SQLITE:
        sqla_event.listen(engine, "connect", event_mngr.emitter("core.db.connect.sqlite"))

    al_cfg = AlConfig()
    al_cfg.set_main_option("script_location", "utmo:alembic")
    al_cfg.set_main_option("sqlalchemy.url", config.db.uri)
    alembic_cmd.upgrade(al_cfg, "head")

    Session = sessionmaker(engine)
    Base.metadata.create_all(engine)
