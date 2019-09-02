import scrapy

class Spider_shiyanlou(scrapy.Spider):
    name = 'shiyanlou-github'

    def start_requests(self):
        url_list = [
                'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjoxMSswODowMM4FkpTJ&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjo1MyswODowMM4FkpKN&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0zMVQyMDoyMDowMiswODowMM4BzHi1&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMi0wNFQwMDoxNzo1MyswODowMM4BpCnu&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0wOS0xNlQxMDowNjowMyswODowMM4Bb3Ud&tab=repositories'
        ]
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for pub in response.xpath('//li[contains(@class, "public")]'):
            yield {
                    'name':pub.xpath('.//h3/a/text()').extract_first().strip(),
                    'update_time':pub.xpath('.//relative-time/@datetime').extract_first()
                    }
