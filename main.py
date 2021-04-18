from data import session
from tools import insert_data
from tools import homeworks

session = session.create()
insert_data.insert(session)

homeworks.number_4(session)
homeworks.number_5(session)
