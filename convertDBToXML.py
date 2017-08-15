import codecs

# Import dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

xml_out = codecs.open('test.xml', 'a', 'utf-8')
xml_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml_out.write('<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')

WCs = session.query(WordClass).all()
lastEntry = session.query(Entry).order_by(Entry.id.desc()).first()
numberOfEntries = lastEntry.id

#for i in range(numberOfEntries):
for i in range(10):
    # Read data from Database
    entry = session.query(Entry).filter_by(id=i+1).one()
    indices = session.query(IndexTag).filter_by(entryId=i+1).all()

    xml_out.write('<d:entry id="' + entry.entryId + '" d:title="' + entry.title + '">\n')
    for index in indices:
        xml_out.write('\t<d:index d:value="' + index.value + '" d:title="' + index.value + '" />\n')

    xml_out.write('\t<h1><span class="headword">' + entry.headword + '</span></h1>\n')

    meanings = session.query(Meaning).filter_by(entryId=i+1).all()
    for meaning in meanings:
        if.meanings.wcId == 0:
            xml_out.write('\t\t<span class="meaning">' + meaning.sentence + '</span>\n')

    xml_out.write('</d:entry>')

xml_out.write('</d:dictionary>\n')
xml_out.close()
