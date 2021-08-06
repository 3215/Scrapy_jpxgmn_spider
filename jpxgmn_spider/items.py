# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JpxgmnSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 自定义所需的 item 字段
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
