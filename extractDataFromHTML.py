import codecs
from tqdm import tqdm

# For Importing dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# 品詞の分類をDBへ保存
def storeWCToDB():
    WCs = ['【動詞＋】', '【＋動詞】', '【形容詞・名詞＋】', '【副詞】', '【副詞１】', \
    '【副詞２】', '【前置詞＋】', '【＋前置詞】', '【雑】', '【＋to do】', '【＋doing】', \
    '【＋that節】', '【＋wh.】', '【＋how】', '【＋that節】【＋補】', '【＋whether】', \
    '【＋whether [if]】', '【＋to do】【＋doing】', '【＋-self】', '【＋補】', '【＋-self】【＋補】']
    for i in range(len(WCs)):
        wordclass = WordClass(type=WCs[i])
        session.add(wordclass)
        session.commit()

# 各アイテムをデータベースへ保存
def storeEntryToDB(entryId, title, headword=None):
    entry = Entry(entryId=entryId, title=title, headword=headword)
    session.add(entry)
    session.commit()

def storeIndexToDB(entryId, value):
    indextag = IndexTag(value=value, entryId=entryId)
    session.add(indextag)
    session.commit()

def storeMeaningToDB(sentence, entryId, wcId):
    meaning = Meaning(sentence=sentence, entryId=entryId, wcId=wcId)
    session.add(meaning)
    session.commit()

# HTML から Entry と Index を抜き出し、データベースへ保存
def extractEntryAndIndex():
    entryIdForIndex = 0
    pbar = tqdm(range(15958))

    for line in f:
        start = line.find("<dt id=")
        # Extract Entry
        if start > -1:
            end = line.find("<a")
            entryId = line[start+8:20]
            title = line[22:end-1]
            storeEntryToDB(entryId, title)
            entryIdForIndex += 1
            pbar.update(1)

        # Extract index
        elif line.find("<key") > -1:
            # Ignore the Kana type and store index into database
            if line.find('type="かな"') < 0:
                end = line.find("type=")
                value = line[12:end-2]
                storeIndexToDB(entryIdForIndex, value)

        elif line.find("&#x01;") > 0:
            break
    f.close()

# HTML から説明文を抜き出し、データベースへ保存
def extractMeaning():
    entryIdForMeaning = 0
    wcId = 0
    pbar = tqdm(range(15958))
    # Extract meanings
    # Extract headword and store into Entry DB
    for line in f:
        if line.find("&#x01;") > 0:
            end = line.find("<br>")
            headword = line[20:end]
            entryIdForMeaning += 1
            entry = session.query(Entry).filter_by(id=entryIdForMeaning).one()
            entry.headword = headword
            session.commit()
            pbar.update(1)

        elif entryIdForMeaning == 0:
            continue

        # Extract subcategory
        elif line.find("&#x02;(") > 0:
            end = line.find("<br>")
            sentence = line[20:end]
            storeMeaningToDB(sentence,entryIdForMeaning, 0)

        # Extract Word Class and save wcId for later
        elif line.find("&#x02;【") > 0:
            end = line.find("<br>")
            wcType = line[20:end]
            wordclass = session.query(WordClass).filter_by(type=wcType).one()
            wcId = wordclass.id

        # Extract the sentense with Link
        elif line.find("&#x02;") > 0 and line.find("cf. <a") > 0:
            end = line.find("<br>")
            sentense = line[20:end]
            storeMeaningToDB(sentence, entryIdForMeaning, wcId)

        # 普通の項目、最初の点は除く
        elif line.find("&#x02;") > 0:
            end = line.find("<a")
            sentence = line[21:end]
            storeMeaningToDB(sentence, entryIdForMeaning, wcId)
    f.close()

# 前処理した HTML からデータを抜き出す
# データベースがすでにある場合は、スキップ（上書き防止）
path = "KENCOLLO.out"
if session.query(WordClass).first() is None:
    storeWCToDB()
if session.query(Entry).first() is None:
    f = codecs.open(path, 'r', 'utf-8')
    print("Start extracting entries and indices.")
    extractEntryAndIndex()
    print("Finished extracting.")
if session.query(Meaning).first() is None:
    f = codecs.open(path, 'r', 'utf-8')
    print("Start extracting items.")
    extractMeaning()
    print("Finished extracting.")
else:
    print("dictionray.db already exists. Delete it if you want to replace.")
