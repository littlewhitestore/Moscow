# *-* coding:utf-8 *-*
import json 
import requests

taobao_id = '560505320361'
name = '琥珀核桃仁 酥脆芝麻核桃仁罐装'
property_key = '规格'
property_value = '红糖口味150g'
price = 1700
market_price = 2800 
banner_img_number = 4
detail_img_number = 8 
image_url_prefix = "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/"

banner_img_list = []
i = 1
while i <= banner_img_number:
    banner_img_list.append(image_url_prefix + "%s_banner_%d.png"%(taobao_id, i))
    i += 1


detail_img_list = []
i = 1
while i <= detail_img_number:
    detail_img_list.append(image_url_prefix + "%s_detail_%d.png"%(taobao_id, i))
    i += 1

payload = {
    'name': name,
    'taobao_id': taobao_id,
    'price': price,
    'market_price': market_price,
    'banner_images': ';'.join(banner_img_list),
    'detail_images': ';'.join(detail_img_list),
}

        
ret = requests.post(
    'https://www.xiaobaidiandev.com/api/goods/upload',
    data=payload 
)
ret_data = json.loads(ret.text)
goods_id = ret_data['data']['goods_id']
print goods_id

payload = {
    'image_url':  banner_img_list[0],
    'price': price,
    'stock': 1000,
    'property_vector_str': "%s|%s"%(property_key, property_value),
}
print payload
ret = requests.post(
    'https://www.xiaobaidiandev.com/api/goods/%d/sku/upload'%goods_id,
    data=payload 
)
#print ret.text