from sqlalchemy import or_, distinct, func

from data.dbase_setup import Performer, Genre, Album, Track, Collection
from tools.time_converter import milliseconds_to_time, time_to_milliseconds

def number_4(session):
    # название и год выхода альбомов, вышедших в 2018 году;
    print('Альбомы вышедшие в 2018 году:')
    result = session.query(Album).filter_by(year=2018).all()
    for record in result:
        print(f"[{record.year}] :: {record.title}")

    # название и продолжительность самого длительного трека;
    print('\nСамый продолжительный трэк:')
    result = session.query(Track).order_by(Track.duration.desc()).first()
    print(f"[{milliseconds_to_time(result.duration)}] :: {result.title}")

    # название треков, продолжительность которых не менее 3,5 минуты;
    print('\nТрэки продолжительностью не менее 3,5 минут:')
    duration = time_to_milliseconds(minutes=3, seconds=30)
    result = session.query(Track).filter(Track.duration >= duration).order_by(Track.duration.desc()).limit(10).all()
    for record in result:
        print(f"[{milliseconds_to_time(record.duration)}] :: {record.title} :: {record.album.title}")

    # названия сборников, вышедших в период с 2018 по 2020 год включительно;
    print('\nСборники вышедшие с 2018 по 2020 годы:')
    result = session.query(Collection).filter(2018 <= Collection.year, Collection.year <= 2020).all()
    for record in result:
        print(f"[{record.year}] :: {record.title}")

    # исполнители, чье имя состоит из 1 слова;
    print('\nИсполнители чьё имя состоит из одного слова:')
    result = session.query(Performer).filter(Performer.name.notlike('%% %%')).all()
    for record in result:
        print(f"{record.name}")

    # название треков, которые содержат слово "мой"/"my".
    print('\nНазвание треков, которые содержат слово "мой"/"my":')
    result = session.query(Track.title).distinct().filter(or_(
        Track.title.op('~*', 0, True)(' my '),
        Track.title.op('~*', 0, True)('^my '))
    ).order_by(Track.title).limit(10).all()

    for record in result:
        print(f"{record.title}")

def number_5(session):
    # количество исполнителей в каждом жанре (сортировка по количеству);
    print('\nКоличество исполнителей в каждом жанре:')
    result = session.query(
        Genre,
        func.count(Performer.id).label('count')).\
        join(Genre.performers).\
        order_by(func.count(Performer.id).desc()).\
        group_by(Genre.id)

    for record in result:
        print(f"{record.Genre.title:.<20}[ {record.count} ]")

    # количество треков, вошедших в альбомы 2019-2020 годов;
    print('\nКоличество треков, вошедших в альбомы 2019-2020 годов:')
    result = session.query(
        func.count(Track.title).label('count')).\
        join(Album).\
        filter(2019 <= Album.year, Album.year <= 2020)
    for record in result:
        print(f"{record.count}")

    # остальные запросы в разработке
