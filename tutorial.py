import scrapy


class TutorialSpider(scrapy.Spider):
    name = 'tutorial'
    allowed_domains = ['tutorial.com']
    start_urls = ['http://tutorial.com/']

    def parse(self, response):
        pass
