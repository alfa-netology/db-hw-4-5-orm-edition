from sqlalchemy import Column, ForeignKey, Integer, String, PrimaryKeyConstraint, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Performer(Base):
    __tablename__ = 'performers'

    extend_existing = True
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)

    genres = relationship("Genre", secondary='performer_genre', backref="performers")
    albums = relationship("Album", secondary='performer_album', back_populates="performers")

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)

    # performers = relationship("Performer", secondary='performer_genre', back_populates="genres")


performer_genre = Table(
    'performer_genre', Base.metadata,
    Column('performer_id', Integer, ForeignKey('performers.id')),
    Column('genre_id', Integer, ForeignKey('genres.id')),
    Column('performer_id', Integer, ForeignKey('performers.id')),
    extend_existing=True,
)

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    year = Column(Numeric(4, 0), nullable=False)

    performers = relationship("Performer", secondary='performer_album', back_populates="albums")


performer_album = Table(
    'performer_album', Base.metadata,
    Column('album_id', Integer, ForeignKey('albums.id')),
    Column('performer_id', Integer, ForeignKey('performers.id'))
)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'))

    album = relationship("Album", backref='tracks')
    collections = relationship("Collection", secondary='track_collection', back_populates="tracks")

class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    year = Column(Numeric(4, 0), nullable=False)

    tracks = relationship("Track", secondary='track_collection', back_populates="collections")

class TrackCollection(Base):
    __tablename__ = 'track_collection'
    __table_args__ = (PrimaryKeyConstraint('track_id', 'collection_id'),)

    track_id = Column(Integer, ForeignKey('tracks.id'))
    collection_id = Column(Integer, ForeignKey('collections.id'))


with open('./data/connection_settings') as file:
    connection_settings = file.readline()

engine = create_engine(connection_settings)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
