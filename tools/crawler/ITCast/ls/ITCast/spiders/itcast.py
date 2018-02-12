#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
from ITCast.items import ItcastItem

class ITCastSpider(scrapy.Spider):

    name = "itcast"
    allowed_domains = ["detail.1688.com"]
    start_urls = ["https://detail.1688.com/offer/528506897951.html"]

    def parse(self, response):

        #商品的尺寸
        property_list = response.xpath('//*[@id="mod-detail-bd"]/div[2]/div[12]/div/div/div/div[2]/div[2]/table/tbody')
                                    # '//*[@id="mod-detail-bd"]/div[2]/div[12]/div/div/div/div[2]/div[2]/table/tbody/tr[1]'

        # 迭代结点列表，获取每个商品的尺寸
        for property in property_list:
            item = ItcastItem()

            item['sku_size'] = property.xpath("tr/td/span/text()").extract()
            yield item





#－－－－－－sku的name　　店铺的name  店铺的url  已完成－－－－－－－－－－－－－－－－－－－－－－－－－－－

#         #sku名称
#         node_list1 = response.xpath('//*[@id="mod-detail-title"]')
#         #店铺名称
#         node_list2 = response.xpath('//*[@id="site_content"]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[1]/div[1]')
#         #商铺的url
#         node_list3 = response.xpath('//*[@id="site_content"]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[1]/div[1]')
#
#         item = ItcastItem()
#
#         # 商品名
#         item['sku_name'] = node_list1.xpath("./h1/text()").extract_first()
#         #店铺名称
#         item['store_name'] = node_list2.xpath("./a/text()").extract_first()
#         #店铺id(可以爬取url）
#         item['store_url'] = node_list3.xpath("./a/@href").extract_first()
#
#         yield item
