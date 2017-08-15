import codecs, re
from tqdm import tqdm

# Import dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

xml_out = codecs.open('KENCOLLO.xml', 'w', 'utf-8')
xml_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml_out.write('<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')

lastEntry = session.query(Entry).order_by(Entry.id.desc()).first()
numberOfEntries = lastEntry.id

pbar = tqdm(range(numberOfEntries))

for i in range(numberOfEntries):
    # Read data from Database
    entry = session.query(Entry).filter_by(id=i+1).one()
    indices = session.query(IndexTag).filter_by(entryId=i+1).all()

    # Write entry
    xml_out.write('<d:entry id="' + entry.entryId + '" d:title="' + entry.title + '">\n')

    # Write indices
    for index in indices:
        xml_out.write('\t<d:index d:value="' + index.value + '" d:title="' + index.value + '" />\n')

    # Write headword
    headword = entry.headword
    if headword.find("<a") > -1:
        headword = headword.replace('href="#', 'href="x-dictionary:r:')
    xml_out.write('\t<h1><span class="headword">' + headword + '</span></h1>\n')

    # Write meanings
    meanings = session.query(Meaning).filter_by(entryId=i+1).all()

    if len(meanings) == 0:
        xml_out.write('</d:entry>\n')
        pbar.update(1)
        continue

    for i in range(len(meanings)):
        wcId = meanings[i].wcId
        sentence = meanings[i].sentence
        # 一つ目の項目 or 小分類
        if wcId == 0 and i == 0:
            xml_out.write('\t<div>\n\t\t<p>' + sentence + '</p>\n')
        elif wcId == 0:
            xml_out.write('\t\t</ul>\n\t</div>\n\t<div>\n\t\t<p>' + sentence + '</p>\n')
        elif i == 0:
            wordclass = session.query(WordClass).filter_by(id = wcId).one()
            xml_out.write('\t<div>\n\t\t<p>' + wordclass.type + '</p>\n\t\t<ul>\n')
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')
        # 普通の項目
        elif wcId == meanings[i-1].wcId:
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')
        # 品詞の変わり目　かつ　直前が小項目
        elif meanings[i-1].wcId == 0:
            wordclass = session.query(WordClass).filter_by(id = wcId).one()
            xml_out.write('\t\t<p>' + wordclass.type + '</p>\n\t\t<ul>\n')
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')
        # 品詞から別の品詞へ切り替え
        else:
            wordclass = session.query(WordClass).filter_by(id = wcId).one()
            xml_out.write('\t\t</ul>\n\t</div>\n\t<div>\n\t\t<p>' + wordclass.type + '</p>\n\t\t<ul>\n')
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')

    xml_out.write('\t\t</ul>\n\t</div>\n</d:entry>\n')
    pbar.update(1)

xml_out.write('</d:dictionary>\n')
xml_out.close()
