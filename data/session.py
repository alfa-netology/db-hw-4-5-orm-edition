from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.dbase_setup import Base

def create():
    engine = create_engine('postgresql://alfa:prime@localhost:5432/muzic_orm')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
