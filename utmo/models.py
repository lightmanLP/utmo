from typing import List
from datetime import datetime

import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import adapters, structures


Base = declarative_base()


class Song(Base):
    __tablename__ = "songs"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    url = sqla.Column(sqla.Text, default="")
    title = sqla.Column(sqla.UnicodeText)
    author = sqla.Column(sqla.UnicodeText)
    description = sqla.Column(sqla.UnicodeText, default="")
    provided_from = sqla.Column(sqla.Integer)
    tags = sqla.Column(sqla.PickleType, default=set)
    plays_count = sqla.Column(sqla.Integer, default=0)
    import_date = sqla.Column(sqla.DateTime, default=datetime.now)
    extra_location_data = sqla.Column(sqla.PickleType, default=None)

    @classmethod
    def export_songs(
        cls,
        with_plays: bool = False,
        with_locals: bool = False
    ) -> List[dict]:
        query = session.query(cls)
        if not with_locals:
            query.filter(cls.provided_from != structures.Providers.LOCAL)
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


engine = sqla.create_engine(adapters.system.db_uri, echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
