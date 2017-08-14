from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Entry
class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    entryId = Column(String(10), index=True)
    title = Column(String(128))

# Index
class Index(Base):
    __tablename__ = 'index'
    id = Column(Integer, primary_key=True)
    value = Column(String(128), nullable=False)
    title = Column(String(128), nullable=False)
    yomi = Column(String(128), nullable=False)
    entryId = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry)

# Categorized by the adjacent word type
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category = Column(String(1000), nullable=False)

# Meaning
class Meaning(Base):
    __tablename__ = 'meaning'
    id = Column(Integer, primary_key=True)
    sentence = Column(String(1000), nullable=False)
    entryId = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry)
    categoryId = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

engine = create_engine('sqlite:///dictionary.db')
Base.metadata.create_all(engine)
