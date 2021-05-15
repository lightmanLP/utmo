import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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
    import_date = sqla.Column(sqla.DateTime)
    extra_location_data = sqla.Column(sqla.PickleType, default=None)


engine = sqla.create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
