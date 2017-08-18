import codecs
import re
import mojimoji
from tqdm import tqdm

# For Importing dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# 一時ファイルのパスを指定
f_temp_path = 'temp.out'

# HTMLファイルの前処理
def pretreat(f_path):

    print('preprocessing HTML file')

    # ファイルの読み込み
    f = codecs.open(f_path, 'r', 'utf-8')
    f_temp = codecs.open(f_temp_path, 'w', 'utf-8')

    for line in f:
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
            f_temp.write(line)
        else:
            f_temp.write("\n" + line)

    f.close()
    f_temp.close()

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

def storeIndexToDB(entryId, value, title):
    indextag = IndexTag(value=value, title=title, entryId=entryId)
    session.add(indextag)
    session.commit()

def storeMeaningToDB(sentence, entryId, wcId):
    meaning = Meaning(sentence=sentence, entryId=entryId, wcId=wcId)
    session.add(meaning)
    session.commit()

# HTML から Entry と Index を抜き出し、データベースへ保存
def extractEntryAndIndex():

    print('Start extracting entry and index')

    # 一時ファイルの読み込み
    f = codecs.open(f_temp_path, 'r', 'utf-8')
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
                value_end = line.find("</key>")
                title_end = line.find("type=")
                value = line[title_end+10:value_end]
                value = mojimoji.zen_to_han(value, kana=False).lower()
                title = line[12:title_end-2]
                storeIndexToDB(entryIdForIndex, value, title)

        elif line.find("&#x01;") > 0:
            break

    f.close()

# HTML から説明文を抜き出し、データベースへ保存
def extractMeaning():

    print("Start extracting items.")
    # 一時ファイルの読み込み
    f = codecs.open(f_temp_path, 'r', 'utf-8')

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

        # Extract word class and save wcId for later
        elif line.find("&#x02;【") > 0:
            end = line.find("<br>")
            wcType = line[20:end]
            wordclass = session.query(WordClass).filter_by(type=wcType).one()
            wcId = wordclass.id

        # 普通の項目、最初の点は除く
        elif line.find("&#x02;") > 0:
            end = line.find("<a")
            sentence = line[21:end]
            storeMeaningToDB(sentence, entryIdForMeaning, wcId)

    f.close()

# linkを削除するための関数
def deleteLink(word):
    word = word.replace("</a>", "")
    a1 = word.find('<a')
    a2 = word.rfind('">')
    word_out = word[:a1] + word[a2+2:]
    return word_out
