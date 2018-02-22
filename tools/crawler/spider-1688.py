import scrapy
import json
import re
import os 
import urllib2

DEFAULT_URLS_CONFIG = os.path.dirname(os.path.realpath(__file__)) + "/1688.txt"
def get_config_url(file=DEFAULT_URLS_CONFIG):
    configure = open(file, 'r').read()
    return configure.split('\n')


class Spider(scrapy.Spider):
    name = '1688'
    start_urls = get_config_url() 

    def parse(self, response):
        #parse title
        title = response.xpath("//h1[@class='d-title']/text()").extract_first()

        #parse cover
        cover_html = response.xpath("//ul/li[contains(@class, 'tab-trigger')]/@data-imgs").extract()
        cover_imgs = []
        for cover in cover_html:
            img = json.loads(cover).get('original', "")
            cover_imgs.append(img)

        #parse sku
        sku_html = ""
        sku_html = re.findall("var iDetailData =(.+?);\n", response.body.decode("GBK"), re.S)[0].replace("\n", "").replace("\t", "")
        sku_json = json.loads(sku_html)
        sku_props = sku_json['sku']['skuProps']
        if len(sku_props) == 0:
            raise Exception("ERROR SKU PROP, IT'S EMPTY:%s"%response.url)
        sku_image_map = {prop['name']:prop.get('imageUrl', "") for prop in sku_props[0]['value']}

        sku = []
        for k, v in sku_json['sku']['skuMap'].items():
            prop_0 = k.split('&gt;')[0]
            image_url = sku_image_map[prop_0] 
            prop = "|".join(k.split('&gt;'))
            stock = v['canBookCount']

            price = v.get('price', None)
            if price == None:
                #if price is between a range
                #using the max price
                #eg: https://detail.1688.com/offer/42635693272.html
                range_price = [p[1] for p in sku_json['sku']['priceRange']]
                price = max(range_price)

            item = {
                "image_url": image_url,
                "price": price,
                "property_vector_str": prop,
                "stock": stock 
            }
            sku.append(item) 

        #parse detail
        detail_url = response.xpath("//div[@id='desc-lazyload-container']/@data-tfs-url").extract()
        detail_url = "https://img.alicdn.com/tfscom/TB1YijBl3vD8KJjSsplXXaIEFXa" 
        detail_response = urllib2.urlopen(detail_url).read()
        detail_imgs = re.findall('src=\\\\"(\S+)\\\\"', detail_response.decode("GBK"))

        id = re.findall('/(\d+).html', response.url)[0]
        result = {
            "id": "%s:%s"%(self.name, id),
            "url": response.url,
            "title": title,
            "cover": cover_imgs,
            "sku": sku,
            "detail": detail_imgs
        }
        return result

