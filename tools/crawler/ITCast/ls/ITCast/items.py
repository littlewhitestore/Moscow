# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItcastItem(scrapy.Item):

    # 商品名称
    sku_name = scrapy.Field()
    # 商品价格
    sku_price = scrapy.Field()
    #店铺名称
    store_name= scrapy.Field()
    # 商品尺寸
    sku_size = scrapy.Field()
    # 商品颜色
    sku_colour = scrapy.Field()
    # 商家id(可以爬取url）
    store_url = scrapy.Field()


