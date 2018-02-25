import json
import re
import os 
import requests

from common.utils import ImageStorage
from tools.crawler.base import BaseSpider


DEFAULT_URLS_CONFIG = os.path.dirname(os.path.realpath(__file__)) + "/url.txt"
HOST = "https://www.xiaobaidiandev.com"
UPLOAD_GOODS_URL = HOST + "/dashboard/goods/upload"
UPLOAD_SKU_URL = HOST + "/dashboard/goods/{goods_id}/sku/upload"


def get_config_url(file=DEFAULT_URLS_CONFIG):
    configure = open(file, 'r').read()
    return configure.split('\n')

def price(original_price):
    return original_price * 100

def upload_to_qcloud(images):
    if isinstance(images, basestring):
        return ImageStorage.upload_from_url(images)

    new_image_keys = []
    for image_url in images:
        object_key = ImageStorage.upload_from_url(image_url)
        new_image_keys.append(object_key)
    return new_image_keys

def upload(goods):
    headers = {'content-type': 'application/json'}
    min_price = min(sku['price'] for sku in goods['sku'])
    banner_image_keys = upload_to_qcloud(goods['cover'])
    detail_image_keys = upload_to_qcloud(goods['detail'])
    payload = {
        'banner_images': ";".join(banner_image_keys),
        'name': goods['title'],
        'market_price': min_price,
        'price': price(min_price),
        'detail_images': ";".join(detail_image_keys),
        'supply_source': goods['id'].split(':')[0],
        'supply_item_id': goods['id'].split(':')[1]
    }
    r = requests.post(UPLOAD_GOODS_URL, data=json.dumps(payload), headers=headers)
    assert r.status_code == 200
    rj = json.loads(r.text)
    goods_id = rj['goods_id']


    for sku in goods['sku']:
        headers = {'content-type': 'application/json'}
        payload = {
            'image_key': upload_to_qcloud(sku['image_url']),
            'price': price(sku['price']),
            'property_vector_str': sku['property_vector_str'],
            'stock': sku['stock'],
        }
        r = requests.post(UPLOAD_SKU_URL.format(goods_id=goods_id), data=json.dumps(payload), headers=headers)
        assert r.status_code == 200


class Spider(BaseSpider):
    name = '1688'
    start_urls = get_config_url() 

    def parse_sku(self, response):
        def parse_from_js_variable(response):
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
                try:
                    if price == None:
                        #eg: https://detail.1688.com/offer/42635693272.html
                        range_price = [p[1] for p in sku_json['sku']['priceRange']]
                        price = max(range_price)
                except Exception, e:
                    pass

                price = float(price)

                item = {
                    "image_url": image_url,
                    "price": price,
                    "property_vector_str": prop,
                    "stock": stock 
                }
                sku.append(item) 
            return sku

        def parse_from_html(response):
            #eg: https://detail.1688.com/offer/539856059524.html?spm=a2615.7691456.0.0.2e267faatnB9jV
            sku = []
            sku_html = response.xpath("//div[contains(@class,'mod-detail-purchasing')]/@data-mod-config").extract_first()
            sku_json = json.loads(sku_html)
            stock = float(sku_json['max'])

            range_price = response.xpath("//span[contains(@class, 'price-length-4')]/text()").extract()
            range_price = [float(p) for p in range_price]
            price = max(range_price)

            item = {
                "image_url": "",
                "price": price,
                "property_vector_str": "",
                "stock": stock 
            }
            sku.append(item) 
            return sku

        try:
            sku = parse_from_js_variable(response)
        except Exception, e:
            sku = []

        if len(sku) == 0:
            try:
                sku = parse_from_html(response)
            except Exception, e:
                sku = []

        return sku


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
        sku = self.parse_sku(response)

        #parse detail
        detail_url = response.xpath("//div[@id='desc-lazyload-container']/@data-tfs-url").extract_first()
        detail_response = requests.get(detail_url)
        try:
            detail_text = detail_response.text.decode(detail_response.encoding)
        except Exception, e:
            detail_text = detail_response.text.decode("utf8")

        detail_imgs = re.findall('src=\\\\"(\S+)\\\\"', detail_text)

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
