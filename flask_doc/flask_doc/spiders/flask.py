# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem
import re

class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    #allowed_domains = ['http://flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/1.0/']

    rules = [
            Rule(
                LinkExtractor(restrict_xpaths=('//div[contains(@class, "toctree-wrapper")]')),
                callback='parse_item',
                follow=True
                )
            ]


    def parse_item(self, response):
        item = PageItem()
        text_html = response.xpath('//text()')
        text = text_html.extract()
        item['text'] = text
        item['url'] = response.url
        yield item


