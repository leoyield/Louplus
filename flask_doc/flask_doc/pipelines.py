# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import json
import re

class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        text = item['text']
        text = [t for t in text if len(t.strip()) > 0]
        text = '\n'.join(text)
        rep = re.findall('\s+', text)
        for i in rep:
            text = text.replace(i, ' ')
        item['text'] = text
        item = json.dumps(dict(item))
        self.redis.lpush('flask_doc:items', item)
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
