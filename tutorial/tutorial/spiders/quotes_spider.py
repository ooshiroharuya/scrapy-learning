import scrapy


class QuotesSpiderSpider(scrapy.Spider):
    # name: 标识当前爬虫。在项目中必须为唯一值。意思就是说，你无法给不同的spider设置相同的name
    name = 'quotes'

    """
    start_request():必须返回一个可迭代的请求Requests（你可以返回一个requests的列表或
    写一个生成器模块）用以给爬虫程序爬取。后续的请求将会从这些初始请求中连续的生成
    """
    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    """
    该方法将会根据每一个生成器生成的请求进行调用，以处理响应的下载。
    处理之后的响应参数是TextResponse的实例。用来存储网页内容，并通过许多有用的方法来处理网页内容。
    parse()方法通常解析响应数据，分离出数据并以字典形式进行存储并同时查找新的url来从中创建新的请求(Request)
    """
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
