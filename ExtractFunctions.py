import codecs
import re
from tqdm import tqdm

# For Importing dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def pretreat(_file, _file_out):
    for line in _file:
        # <nobr>, <sub>, <sup> タグを全削除する
        line = line.replace("<nobr>", "").replace("</nobr>", "")
        line = line.replace("<sub>", "").replace("</sub>", "")
        line = re.sub('<sup>(.+?)</sup>', '', line)

        # 半角文字前の全角数字を削除する
        line = re.sub('[０-９]([a-xA-Z0-9_])', '\\1', line)

        # 全角スペースを半角スペースに変換する
        line = line.replace("　", " ")

        # 不要な改行を削除する
        line = line.replace("\n", "")
        if line.find(" ") == 0 :
            _file_out.write(line)
        else:
            _file_out.write("\n" + line)

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
def extractEntryAndIndex(_file):
    entryIdForIndex = 0
    pbar = tqdm(range(15958))

    for line in _file:
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

# HTML から説明文を抜き出し、データベースへ保存
def extractMeaning(_file):
    entryIdForMeaning = 0
    wcId = 0
    pbar = tqdm(range(15958))
    # Extract meanings
    # Extract headword and store into Entry DB
    for line in _file:
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
