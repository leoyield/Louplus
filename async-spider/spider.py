import asyncio
import aiohttp
import csv
import async_timeout
from scrapy.http import HtmlResponse

results = []

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

def parse(url, body):
    response = HtmlResponse(url=url, body=body.encode('utf8'))
    for re in response.xpath('//li[@itemprop="owns"]'):

        name = re.xpath('.//h3/a/text()').extract_first().strip()
        update_time = re.xpath('.//relative-time/@datetime').extract_first()

        results.append((name, update_time))

async def task(url):
    async with aiohttp.ClientSession() as session:
        body = await fetch(session, url)
        parse(url, body)

def main():
    loop = asyncio.get_event_loop()
    url_list = [
            'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjoxMSswODowMM4FkpTJ&tab=repositories'
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjo1MyswODowMM4FkpKN&tab=repositories'
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0zMVQyMDoyMDowMiswODowMM4BzHi1&tab=repositories'
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMi0wNFQwMDoxNzo1MyswODowMM4BpCnu&tab=repositories'
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0wOS0xNlQxMDowNjowMyswODowMM4Bb3Ud&tab=repositories'
            ]
        
    tasks = [task(url) for url in url_list]
    loop.run_until_complete(asyncio.gather(*tasks))
    with open('shiyanlou-repos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

if __name__ == '__main__':
    main()
