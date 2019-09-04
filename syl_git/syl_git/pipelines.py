# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from syl_git.models import Repository, engine
from sqlalchemy.orm import sessionmaker

class SylGitPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.datetime.strptime(
                item['update_time'],
                '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=8)
        item['commits'] = int(item['commits'].replace(',', ''))
        item['branches'] = int(item['branches'].replace(',', ''))
        item['releases'] = int(item['releases'].replace(',', ''))
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
