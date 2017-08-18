#import sqlite3
#connect = sqlite3.connect("dictionary.db")
#c = connect.cursor()
#c.execute("SELECT * FROM IndexTag order by id limit 10")
#print(c.fetchall())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

entry = session.query(Entry).filter_by(entryId='0003804D03D0').one()
meaning = session.query(Meaning).filter_by(entryId='8566').all()

for i in meaning:
    print(i.sentence)
