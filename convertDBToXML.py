import codecs, re
from tqdm import tqdm
from functions import deleteLink

# データベースを呼び出す
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, Entry, WordClass, Meaning, IndexTag
engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# 出力するファイルを設定
xml_out = codecs.open('KENCOLLO.xml', 'w', 'utf-8')
xml_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml_out.write('<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')

# Entryの数を数える
lastEntry = session.query(Entry).order_by(Entry.id.desc()).first()
numberOfEntries = lastEntry.id

# 変換プロセスの可視化
pbar = tqdm(range(numberOfEntries))

# データベース上のエントリーを出力する
for i in range(numberOfEntries):

    # データベースからエントリーとインデックスを読み込み
    entry = session.query(Entry).filter_by(id=i+1).one()
    indices = session.query(IndexTag).filter_by(entryId=i+1).all()

    # エントリー名を書く
    xml_out.write('<d:entry id="' + entry.entryId + '" d:title="' + entry.title + '">\n')

    # Indexを書く
    for index in indices:
        xml_out.write('\t<d:index d:value="' + index.value + '" d:title="' + index.title + '" />\n')

    # 検索結果の頭の表記を書く
    headword = entry.headword
    if headword.find("<a") > -1:
        headword = deleteLink(headword)
    xml_out.write('\t<h1><span class="headword">' + headword + '</span></h1>\n')

    # データベースから説明文を読み込み
    meanings = session.query(Meaning).filter_by(entryId=i+1).all()

    # 説明文が無い場合は、エントリーを閉じて次の項目へ行こう
    if len(meanings) == 0:
        xml_out.write('</d:entry>\n')
        pbar.update(1)
        continue

    # 説明文を出力
    for i in range(len(meanings)):
        wcId = meanings[i].wcId
        sentence = meanings[i].sentence

        if sentence.find("<a") > -1:
            sentence = deleteLink(sentence)

        # 最初　かつ　小分類（１）（２）...がある場合
        if wcId == 0 and i == 0:
            xml_out.write('\t<div>\n\t\t<p>' + sentence + '</p>\n')

        # 最後に小分類がある場合
        elif wcId == 0 and i == len(meanings)-1:
            xml_out.write('\t\t</ul>\n\t</div>\n\t<div>\n\t\t<p>' + sentence + '</p>\n\t\t<ul>\n')

        # 小分類
        elif wcId == 0:
            xml_out.write('\t\t</ul>\n\t</div>\n\t<div>\n\t\t<p>' + sentence + '</p>\n')

        # 説明文の最初、【品詞】＋説明文
        elif i == 0:
            wordclass = session.query(WordClass).filter_by(id = wcId).one()
            xml_out.write('\t<div>\n\t\t<p>' + wordclass.type + '</p>\n\t\t<ul>\n')
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')

        # 説明文のみ記載
        elif wcId == meanings[i-1].wcId:
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')

        # 直前が小分類 の場合
        elif meanings[i-1].wcId == 0:
            wordclass = session.query(WordClass).filter_by(id = wcId).one()
            xml_out.write('\t\t<p>' + wordclass.type + '</p>\n\t\t<ul>\n')
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')

        # 品詞が切り替わるタイミング
        else:
            wordclass = session.query(WordClass).filter_by(id = wcId).one()
            xml_out.write('\t\t</ul>\n\t</div>\n\t<div>\n\t\t<p>' + wordclass.type + '</p>\n\t\t<ul>\n')
            xml_out.write('\t\t\t<li>' + sentence + '</li>\n')

    # エントリーを閉じる
    xml_out.write('\t\t</ul>\n\t</div>\n</d:entry>\n')

    # tqdm を使って進捗を示す
    pbar.update(1)

# 辞書を閉じる
xml_out.write('</d:dictionary>\n')
xml_out.close()
