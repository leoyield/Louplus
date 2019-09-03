# -*- coding: utf-8 -*-
import scrapy


class RepositorySpider(scrapy.Spider):
    name = 'repository'
    #allowed_domains = ['github.com']
    @property
    def start_urls(self):
        url_list = [
                'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjoxMSswODowMM4FkpTJ&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjo1MyswODowMM4FkpKN&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0zMVQyMDoyMDowMiswODowMM4BzHi1&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMi0wNFQwMDoxNzo1MyswODowMM4BpCnu&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0wOS0xNlQxMDowNjowMyswODowMM4Bb3Ud&tab=repositories'
                ]
        return url_list

    def parse(self, response):
        for repos in response.xpath('//li[contains(@class, "public")]'):
            yield {
            'name': repos.xpath('.//h3/a/text()').extract_first().strip(),
            'update_time': repos.xpath('.//relative-time/@datetime').extract_first().strip()
            }
