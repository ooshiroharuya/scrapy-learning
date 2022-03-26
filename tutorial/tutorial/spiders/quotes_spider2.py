import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes2"
    start_url = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]
    
    def parse(self, response):
        page = response.url.spit("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            