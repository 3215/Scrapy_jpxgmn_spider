import scrapy
from urllib import parse
from ..items import JpxgmnSpiderItem


class JpxgmnSpider(scrapy.Spider):
    name = 'jpxgmn'
    allowed_domains = ['www.jpmn5.com']
    start_urls = ['http://www.jpmn5.com/']
    resource_url = 'https://p.jpmn5.com/'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36'}

    def parse(self, response):
        # 通过主站获取各个系列的 url
        menu_item = response.xpath("//ul[@class='sub-menu']//*[@class='menu-item']/a/@href").extract()[42:43]
        for item in menu_item:
            item_url = parse.urljoin(response.url, item)

            yield scrapy.Request(url=item_url, headers=self.header, callback=self.parse_1, dont_filter=True)   # 传给 parse_1 回调函数进行进一步处理

    def parse_1(self, response):
        # 通过系列页面获取各个图组的 url
        related_box = response.xpath("//*[@class='related_box']/a/@href").extract()[:3]    # [:n]调节爬取页面数量
        for box in related_box:
            box_url = parse.urljoin(response.url, box)
            yield scrapy.Request(url=box_url, headers=self.header, callback=self.find_img_url, dont_filter=True)   # 传给 find_img_url 回调函数进行解析

        # next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract_first('')
        # yield scrapy.Request(url=parse.urljoin(response.url, next_page), callback=self.parse_1)
        # 通过该系列页面获得下一页的 url ,并传给回调函数进行以上处理

    def find_img_url(self, response):
        image_info = JpxgmnSpiderItem()    # 实例化 item 对象
        image_info["image_paths"] = response.xpath("//*[@class='article-title']/text()").extract_first('')

        img_urls = response.xpath("//p/img/@src").extract()
        image_urls = []    # 待下载的图片url列表（必须为列表）
        for img_url in img_urls:
            img_url = '/U' + img_url[2:]
            img_url = parse.urljoin(self.resource_url, img_url)
            image_urls.append(img_url)
        image_info["image_urls"] = image_urls

        yield image_info    # 将赋值好了的 item 传出去

        next_url = response.xpath("//a[contains(text(), '下一页')]/@href").extract_first('')
        yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.find_img_url)
        # 通过该图片页面获得下一页的 url ,并传给回调函数进行以上处理




