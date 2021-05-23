from typing import List
from datetime import datetime

import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from alembic import command, config

from . import adapters, structures


Base = declarative_base()
engine: "sqla.engine.Engine"
Session: "sessionmaker"
session: "Session"


association = sqla.Table(
    "association",
    Base.metadata,
    sqla.Column("song_id", sqla.Integer, sqla.ForeignKey("songs.id"), primary_key=True),
    sqla.Column("tag", sqla.Integer, sqla.ForeignKey("tags.tag"), primary_key=True)
)


class Song(Base):
    __tablename__ = "songs"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    url = sqla.Column(sqla.Text, default="")
    title = sqla.Column(sqla.UnicodeText)
    author = sqla.Column(sqla.UnicodeText)
    description = sqla.Column(sqla.UnicodeText, default="")
    provider = sqla.Column(sqla.Integer)
    plays_count = sqla.Column(sqla.Integer, default=0)
    import_date = sqla.Column(sqla.DateTime, default=datetime.now)
    extra_location_data = sqla.Column(sqla.PickleType, default=None)

    tags = relationship("Tag", secondary=association, back_populates="songs")

    def __repr__(self) -> str:
        return f"{self.title} {chr(8212)} {self.author}"

    @classmethod
    def export_songs(
        cls,
        with_plays: bool = False,
        with_locals: bool = False
    ) -> List[dict]:
        query = session.query(cls)
        if not with_locals:
            query.filter(cls.provider != structures.Providers.LOCAL)
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

    tag = sqla.Column(sqla.UnicodeText, primary_key=True)

    songs = relationship("Song", secondary=association, back_populates="tags")

    def __repr__(self) -> str:
        return self.tag


def init():
    global engine, Session, session

    engine = sqla.create_engine(adapters.system.db_uri, echo=False)

    al_cfg = config.Config()
    al_cfg.set_main_option("script_location", "utmo:alembic")
    al_cfg.set_main_option("sqlalchemy.url", adapters.system.db_uri)
    command.upgrade(al_cfg, "head")

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
