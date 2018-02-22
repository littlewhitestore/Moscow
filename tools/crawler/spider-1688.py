import scrapy
import json
import re
import os 
import urllib2
import requests

DEFAULT_URLS_CONFIG = os.path.dirname(os.path.realpath(__file__)) + "/1688.txt"
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
        detail_response = urllib2.urlopen(detail_url).read()
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



if __name__ == "__main__":
    goods = {'sku': [{'property_vector_str': u'\u989c\u8272|\u8fd0\u8d39\u8865\u5dee', 'price': 1.0, 'image_url': '', 'stock': 9702}, {'property_vector_str': u'\u989c\u8272|\u4e09\u89d2\u5dfe\u6253\u7248', 'price': 280.0, 'image_url': '', 'stock': 944}, {'property_vector_str': u'\u989c\u8272|\u5a74\u513f\u88c5', 'price': 300.0, 'image_url': '', 'stock': 999}], 'title': u'\u5a74\u513f\u670d\u9970 \u7eaf\u68c9\u4e09\u89d2\u5dfe\u5916\u8d38\u53e3\u6c34\u5dfe\u52a0\u5de5\u5b9a\u5236 \u6253\u7248\u94fe\u63a5 \u8fd0\u8d39\u8865\u5dee\u94fe\u63a5', 'url': 'https://detail.1688.com/offer/528705387116.html', 'cover': [u'https://cbu01.alicdn.com/img/ibank/2016/295/599/3011995592_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/557/236/3012632755_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/263/917/2868719362_1031861432.jpg'], 'detail': [u'https://cbu01.alicdn.com/img/ibank/2015/887/162/2561261788_1778072454.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/296/064/3013460692_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/703/333/3015333307_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/087/328/3012823780_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/053/723/3015327350_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/609/718/3012817906_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/805/364/3013463508_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/117/601/3076106711_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/480/415/3077514084_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/517/028/3012820715_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/478/423/3015324874_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/791/033/3015330197_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/879/123/3015321978_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/201/115/3077511102_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/480/535/3075535084_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/791/211/3076112197_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/777/466/3125664777_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/786/454/3124454687_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/053/459/2661954350_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/038/188/2657881830_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/720/069/2661960027_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/392/159/2661951293_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/621/711/2660117126_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/746/488/2657884647_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/370/759/2661957073_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2015/039/549/2661945930_1031861432.jpg', u'https://cbu01.alicdn.com/img/ibank/2016/384/515/2723515483_1031861432.jpg'], 'id': '1688:528705387116'}
    upload(goods)
