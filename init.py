import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine("sqlite:///scratchData.db")
Session = sessionmaker(bind=engine)
metaData = db.MetaData()
Base = declarative_base()


def init():
    Base.metadata.create_all(engine)