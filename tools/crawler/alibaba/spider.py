import scrapy
import json
import re
import os 
import requests

DEFAULT_URLS_CONFIG = os.path.dirname(os.path.realpath(__file__)) + "/url.txt"
def get_config_url(file=DEFAULT_URLS_CONFIG):
    configure = open(file, 'r').read()
    return configure.split('\n')

def price(original_price):
    return original_price * 100

def upload(goods):
    #https://github.com/littlewhitestore/Moscow/wiki/7.%E5%95%86%E5%93%81%E4%B8%8A%E4%BC%A0
    HOST = "https://www.xiaobaidiandev.com"
    UPLOAD_GOODS_URL = HOST + "/api/goods/upload"
    UPLOAD_SKU_URL = HOST + "/api/goods/{goods_id}/sku/upload"
    headers = {'content-type': 'application/json'}
    min_price = min(sku['price'] for sku in goods['sku'])
    payload = {
        'banner_images': ";".join(goods['cover']),
        'name': goods['title'],
        'market_price': min_price,
        'price': price(min_price),
        'detail_images': ";".join(goods['detail']),
        'supply_source': goods['id'].split(':')[0],
        'supply_item_id': goods['id'].split(':')[1]
    }
    r = requests.post(UPLOAD_GOODS_URL, data=json.dumps(payload), headers=headers)
    rj = json.loads(r.text)
    goods_id = rj['data']['goods_id']


    for sku in goods['sku']:
        headers = {'content-type': 'application/json'}
        payload = {
            'image_url': sku['image_url'],
            'price': price(sku['price']),
            'property_vector_str': sku['property_vector_str'],
            'stock': sku['stock'],
        }
        r = requests.post(UPLOAD_SKU_URL.format(goods_id=goods_id), data=json.dumps(payload), headers=headers)
        print r


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
        sku_prop_map = {}
        for i in range(0, len(sku_props)):
            for item in sku_props[i]['value']:
                k = item['name']
                v = sku_props[i]['prop']
                sku_prop_map[k] = v

        sku = []
        for k, v in sku_json['sku']['skuMap'].items():
            prop_0 = k.split('&gt;')[0]
            image_url = sku_image_map[prop_0] 
            prop = "|".join(["%s|%s"%(sku_prop_map[p], p) for p in k.split('&gt;')])
            stock = v['canBookCount']

            price = v.get('price', None)
            if price == None:
                #if price is between a range
                #using the max price
                #eg: https://detail.1688.com/offer/42635693272.html
                range_price = [p[1] for p in sku_json['sku']['priceRange']]
                price = max(range_price)
            price = float(price)

            item = {
                "image_url": image_url,
                "price": price,
                "property_vector_str": prop,
                "stock": stock 
            }
            sku.append(item) 

        #parse detail
        detail_url = response.xpath("//div[@id='desc-lazyload-container']/@data-tfs-url").extract_first()
        detail_response = requests.get(detail_url).text
        detail_imgs = re.findall('src=\\\\"(\S+)\\\\"', detail_response.decode("GBK"))

        id = re.findall('/(\d+).html', response.url)[0]
        goods = {
            "id": "%s:%s"%(self.name, id),
            "url": response.url,
            "title": title,
            "cover": cover_imgs,
            "sku": sku,
            "detail": detail_imgs
        }
        upload(goods)
        return goods 
