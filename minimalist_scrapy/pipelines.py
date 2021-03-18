# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from minimalist_scrapy.models import (
    Quote, Author, Tag, db_connect, create_table
)
import logging

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MinimalistScrapyPipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeLine:
    def __init__(self):
        """
        Initialize database connection
        create Table
        """
        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker(bind=engine)
        logging.info(
            "****DuplicatesPipeLine: database connection established****"
        )

    def process_item(self, item, spider):
        """
        Prosess the item
        """
        session = self.session()
        quote_exists = session.query(
            Quote
        ).filter_by(text=item.get('text')).first()
        if quote_exists is not None:
            raise DropItem(f"Duplicate item found: f{item.get('text')}")
            session.close()
        else:
            return item
            session.close()


class SaveQuotesPipeline(object):
    """
    Save quotes
    """
    def __init__(self):
        """
        Intiialize database connection and session maker
        Creates Table
        """
        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker(bind=engine)
        logging.info("****SaveQuotePipeline: database connected")


    def process_item(self, item, spider):
        """
        Save the quotes to database
        This method is called for every item pipeline component
        """
        session = self.session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item.get('name')
        author.birthday = item.get('birthday')
        author.born_location = item.get('born_location')
        author.bio = item.get('bio')
        quote.text = item.get('text')
        author_exists = session.query(
            Author
        ).filter_by(name=author.name).first()

        if author_exists is not None:
            quote.author = author_exists
        else:
            quote.author = author


        if 'tags' in item:
            for tag_name in item.get('tags', []):
                tag = Tag(name=tag_name)
                tag_exists = session.query(
                    Tag
                ).filter_by(name=tag_name).first()
                if tag_exists is not None:
                    tag = tag_exists
                quote.tags.append(tag)

        try:
            session.add(quote)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item



