# -*- coding: utf-8 -*-
import scrapy


class RepositorySpider(scrapy.Spider):
    name = 'repository'
    #allowed_domains = ['github.com']
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for repos in response.xpath('//li[contains(@class, "public")]'):
            item = {
            'name': repos.xpath('.//h3/a/text()').extract_first().strip(),
            'update_time': repos.xpath('.//relative-time/@datetime').extract_first().strip()
            }
            summary_url = repos.xpath('.//a/@href').extract_first()
            full_summary_url = response.urljoin(summary_url)
            
            request = scrapy.Request(full_summary_url, self.parse_repository)
            request.meta['item'] = item

            yield request
            
            for url in response.xpath('//div[@class="BtnGroup"]/a[text()="Next"]/@href').extract():
                yield scrapy.Request(url=url, callback=self.parse)


    def parse_repository(self, response):
        item = response.meta['item']

        item['commits'] = response.css('div.overall-summary span::text').extract()[0].strip()
        item['branches'] = response.css('div.overall-summary span::text').extract()[1].strip()
        item['releases'] = response.css('div.overall-summary span::text').extract()[2].strip()

        yield item

