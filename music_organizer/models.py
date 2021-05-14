import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = sqla.create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()


class Song:
    __tablename__ = "songs"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    url = sqla.Column(sqla.Text)
    title = sqla.Column(sqla.UnicodeText)
    author = sqla.Column(sqla.UnicodeText)
    description = sqla.Column(sqla.UnicodeText)
    provided_from = sqla.Column(sqla.Integer)
    tags = sqla.Column(sqla.PickleType)
    import_date = sqla.Column(sqla.DateTime)
    ydl_paths = sqla.Column(sqla.PickleType)


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
