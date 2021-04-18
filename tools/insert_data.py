import json
import random

from sqlalchemy import func
from data.dbase_setup import Performer, Genre, PerformerGenre, Album, PerformerAlbum, Track, TrackCollection, \
    Collection

def insert(session):

    with open('./data/performers_data.json', encoding='utf-8') as file:
        performers_data = json.load(file)

    genres_id = 0
    album_id = 0
    track_id = 0
    genres = {}

    for performer_id, (performer_name, performer_data) in enumerate(performers_data.items()):
        record = Performer(id=performer_id, name=performer_name)
        session.add(record)

        for genre in performer_data.get('genres'):
            if genre not in genres:
                session.add(Genre(id=genres_id, title=genre))
                genres[genre] = genres_id
                genres_id += 1

            genre_id = session.query(Genre).filter_by(title=genre).one().id
            session.add(PerformerGenre(genre_id=genre_id, performer_id=performer_id))

        for album in performer_data.get('albums'):
            album_title = album.get('title').replace("'", "''")
            album_year = album.get('year')
            if album_year != '0':
                session.add(Album(id=album_id, title=album_title, year=album_year))
                session.add(PerformerAlbum(album_id=album_id, performer_id=performer_id))

                for track in album.get('tracks'):
                    track_title = track.get('title').replace("'", "''")
                    track_duration = int(track.get('duration'))
                    session.add(Track(id=track_id, title=track_title, duration=track_duration, album_id=album_id))
                    track_id += 1
                album_id += 1
        session.commit()

    max_track_id = session.query(func.max(Track.id)).scalar()

    for collection_id in range(11):
        collection_year = random.randrange(2015, 2022, 1)
        collection_title = f"Collection #{collection_id}"
        session.add(Collection(id=collection_id, title=collection_title, year=collection_year))

        for i in range(random.randrange(10, 15, 1)):
            track_id = random.sample(range(0, max_track_id), 1)[0]
            existing_track_id = session.query(TrackCollection).filter_by(track_id=track_id).first()
            session.commit()
            if existing_track_id is None:
                session.add(TrackCollection(track_id=track_id, collection_id=collection_id))
                session.commit()
