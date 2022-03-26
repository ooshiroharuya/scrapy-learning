# scrapy-learning
正式开始自己的scrapy学习之旅



## Scrapy 教程

在这个教程中，我们默认Scrapy 已经安装到您的系统中。如果还没有到达这一步，请查看安装指南。

我们将要爬取的网站是 [名人名言](https://quotes.toscrape.com/)。

该教程将带领你完成一下几个任务：

1. 创建一个新的Scrapy 项目
2. 写一个 spider 来爬去网站以及切割出想要的数据。
3. 通过命令行导出想要的数据
4. 改变 spider 来递归爬取后续链接
5. 使用 spider 参数

Scrapy 使用python语言编写。如果你对这个语言还一无所知，你可以通过这个爬虫小项目来对python语言来开始你的python学习之旅。

如果你已经熟悉其他不同的语言，想要快速掌握python，查看[官方文档](https://docs.python.org/zh-cn/3/tutorial/)是一个不错的选择。

如果你刚开始编程并且想以python作为第一个语言，以下基本书可能会对你有所帮助：



## 创建项目

在你开始爬虫之前，你得先创建一个Scrapy项目。进入一个你想要存储代码的文件夹然后执行下列命令：

```shell
scrapy startproject tutorial // tutorial 非固定名称，可以自己取名
```

执行完成之后将会创建一个`tutorial` 文件夹以及以下内容：

```
tutorial/
    scrapy.cfg            # 部署配置文件

    tutorial/             # 项目的python模块，从这里导入代码
        __init__.py

        items.py          # 项目对象定义文件

        middlewares.py    # 项目中间件文件

        pipelines.py      # 项目通道文件

        settings.py       # 项目设置文件

        spiders/          # 稍后放置爬虫文件的文件夹
            __init__.py
```



## 我们的第一个爬虫

爬虫是你定义给Scrapy用于从网页中爬取信息的类（或者一组网页）。他们必须继承 `Spider` 并且定义需要执行的初始请求，也可以配置一下在页面中查找链接的方式、如何解析下载的页面内容来获得数据。

这是我们第一个爬虫的代码，以`qutoes_spider.py`为文件名将该代码保存到你项目的`tutorial/spiders` 文件夹下：

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
```

如你所见，我们的Spider继承自`scrapy.spider` 并定义了一些属性和方法：

* `name`：标识Spider。在该项目中 `name` 必须为唯一值，意味着你无法给不同的Spider设置相同的名字。

* `start_requests()`：必须返回一个可迭代的Requests（你可以返回一个requests的list或者写一个生产者函数）用于给Spider提供爬取的路径。之后的请求将可以从这些初始请求迭代产生。

* `parse()`：该方法可以被调用处理每一个请求的响应数据。响应参数为`TextResponse`的实例，可以用于存储页面内容并提供一系列有用的方法来处理数据。

  `parse()`方法通常用于解析响应参数，提取需要的数据作为字典并查找新的url来爬取。



## 如何运行爬虫

要让我们的爬虫开始工作，在项目的根目录运行以下命令：

```shell
scrapy crawl quotes
```

该命令将执行我们之前所添加`name` 为`qutoes`的爬虫，爬虫会向`quotes.toscrape.com` 网站发送一些请求。你可以获得一些像下面这样的输出参数：

```
... (omitted for brevity)
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Spider opened
2016-12-16 21:24:05 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2016-12-16 21:24:05 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://quotes.toscrape.com/robots.txt> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/1/> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/2/> (referer: None)
2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-1.html
2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-2.html
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Closing spider (finished)
...
```

现在，在当前目录中检查文件。你会注意到有两个新文件被创建出来了:*quotes-1.html* 和 *quotes-2.html*，每个html文件都存储着各自url的内容，这就是我们`parse` 方法做到的。

> 如果你在想为什么我们还没有解析这些HTML，别着急，我们马上就把解析这一块也包含进来



## 刚刚的命令到底做了什么？

Scrapy会将该spider的`start_requests`方法返回的`scrapy.Request`对象进行安排处理。每一次收到响应之后，它实例化 Response 对象并调用与请求关联的回调方法（在本例中为 parse 方法），将响应作为参数传递。



## start_request 方法的快捷方式

你可以通过定义一个装着url的列表的名称为`start_urls` 的类属性，来替代实现用于生成`scrapy.Requests`对象的`start_requests()`方法。这个列表将会被默认的`start_requests()` 的实现方法来调用创建一些初始化的requests给你的爬虫：

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
```

