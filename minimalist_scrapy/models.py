from sqlalchemy import (
    create_engine, Column, Table, ForeignKey, MetaData,
    Integer, String, Date, DateTime, Float, Boolean, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from scrapy.utils.project import get_project_settings


Base = declarative_base()


def db_connect():
    """
    Performs database connection based on settings from settings.py.
    returns sqlalchemy engine instance.
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)


quote_tag = Table(
    'quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quote.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Quote(Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True)
    text = Column('quote_content', Text())
    author_id = Column(Integer, ForeignKey('author.id'))
    tags = relationship(
        'Tag', secondary='quote_tag',
        lazy='dynamic', backref='quote'
    )


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    birthday = Column('birthday', DateTime)
    born_location = Column('born_location', String(150))
    bio = Column('bio', Text())
    quotes = relationship(
        'Quote', backref='author'
    )


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    quotes = relationship(
        'Quote', secondary='quote_tag',
        lazy='dynamic', backref="tag"
    )

