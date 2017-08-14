import codecs

# Import dictionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Entry, Category, Meaning, Index

engine = create_engine('sqlite:///dictionary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Extract category type from HTML file
f = codecs.open('KENCOLLO2', 'r', 'utf-8')
categories = []
for line in f:
    start = line.rfind("【")
    if start > 0:
        end = line.rfind("】")
        category = line[start:end+1]
        if category not in categories:
            print(category)
            categories.append(category)
f.close()

# Add to the DB
for i in range(len(categories)):
    category = Category(category=categories[i])
    session.add(category)
    session.commit()

# categories = ["【動詞＋】", "【前置詞＋】", "【副詞】", "【形容詞・名詞＋】", "【副詞１】", "【＋前置詞】", "【雑】", "【＋-self】", "【＋動詞】", "【＋doing】", "【＋to do】", "【＋that節】", "【＋補】", "【＋wh.】", "【副詞２】", "【＋whether】", "【＋whether [if]】", "【＋how】"]
