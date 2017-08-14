import codecs
import re

# Import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Entry, Category, Meaning, Index
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

f = codecs.open('test', 'r', 'utf-8')
f_out = codecs.open('test_out', 'a', 'utf-8')

for line in f:
    # remove all <nobr></nobr>
    line = line.replace("<nobr>", "").replace("</nobr>", "")



    # remove link to the parent words
    line = re.sub('<a href="#[0-9A-Fa-f]{12}">&#xE00C;</a>', '', line)
    f_out.write(line)
f.close()
f_out.close()
