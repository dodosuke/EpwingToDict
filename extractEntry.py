import codecs

# Import dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Entry, Category, Meaning, IndexTag

engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Store data to DB
def storeCategoryToDB():
    categories = ['【動詞＋】', '【＋動詞】', '【形容詞・名詞＋】', '【副詞】', '【副詞１】', \
    '【副詞２】', '【前置詞＋】', '【＋前置詞】', '【雑】', '【＋to do】', '【＋doing】', \
    '【＋that節】', '【＋wh.】', '【＋how】', '【＋that節】【＋補】', '【＋whether】', \
    '【＋whether [if]】', '【＋to do】【＋doing】', '【＋-self】', '【＋補】', '【＋-self】【＋補】']
    for i in range(len(categories)):
        category = Category(category=categories[i])
        session.add(category)
        session.commit()

def storeEntryToDB(entryId, title, headword=None):
    entry = Entry(entryId=entryId, title=title, headword=headword)
    session.add(entry)
    session.commit()

def storeIndexToDB(entryId, value):
    indextag = IndexTag(value=value, entryId=entryId)
    session.add(indextag)
    session.commit()

def storeMeaningToDB(sentence, entryId, categoryId):
    meaning = Meaning(sentence=sentence, entryId=entryId, categoryId=categoryId)
    session.add(meaning)
    session.commit()

def printProgress(inputId):
    if inputId % 200 == 0:
        print(inputId)

def extractEntryAndIndex():
    entryIdForIndex = 0

    for line in f:
        start = line.find("<dt id=")
        # Extract Entry
        if start >= 0:
            end = line.find("<a")
            entryId = line[start+8:20]
            title = line[22:end-1]
            storeEntryToDB(entryId, title)
            entryIdForIndex += 1
            printProgress(entryIdForIndex)

        # Extract index
        elif line.find("<key") >= 0:
            # Ignore the Kana type
            if line.find('type="かな"') < 0:
                end = line.find("type=")
                value = line[12:end-2]
                storeIndexToDB(entryIdForIndex, value)

        # Extract meanings
        elif line.find("&#x01;") > 0:
            break
    f.close()

def extractMeaning():
    entryIdForMeaning = 0
    categoryId = 0

    for line in f:
        if line.find("&#x01;") >0:
            end = line.find("<br>")
            headword = line[20:end]
            entryIdForMeaning += 1
            entry = session.query(Entry).filter_by(id=entryIdForMeaning).one()
            entry.headword = headword
            session.commit()
            printProgress(entryIdForMeaning)
        elif line.find("&#x02;【") > 0 and entryIdForMeaning > 0:
            end = line.find("<br>")
            categoryName = line[20:end]
            category = session.query(Category).filter_by(category=categoryName).one()
            categoryId = category.id
        elif line.find("&#x02;") > 0 and entryIdForMeaning > 0:
            end = line.find("<a")
            sentence = line[20:end]
            storeMeaningToDB(sentence, entryIdForMeaning, categoryId)
    f.close()

#session.query(Category).delete()
#session.commit()
if session.query(Category).first() is None:
    storeCategoryToDB()
if session.query(Entry).first() is None:
    f = codecs.open('KENCOLLO2', 'r', 'utf-8')
    extractEntryAndIndex()
if session.query(Meaning).first() is None:
    f = codecs.open('KENCOLLO2', 'r', 'utf-8')
    extractMeaning()
