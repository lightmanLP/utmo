from typing import List

import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import adapters


Base = declarative_base()


class Song(Base):
    __tablename__ = "songs"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    url = sqla.Column(sqla.Text)
    title = sqla.Column(sqla.UnicodeText)
    author = sqla.Column(sqla.UnicodeText)
    description = sqla.Column(sqla.UnicodeText)
    provided_from = sqla.Column(sqla.Integer)
    tags = sqla.Column(sqla.PickleType)
    plays_count = sqla.Column(sqla.Integer)
    import_date = sqla.Column(sqla.DateTime)
    extra_location_data = sqla.Column(sqla.PickleType, default=None)

    @classmethod
    def export_songs(cls) -> List[dict]:
        ...  # TODO

    @classmethod
    def import_songs(cls, data: List[dict]):
        ...  # TODO


engine = sqla.create_engine(adapters.system.db_uri, echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
