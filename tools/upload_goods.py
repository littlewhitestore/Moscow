# *-* coding:utf-8 *-*
import json 
import requests

taobao_id = '45248183806'
name = '蜜饯果脯 芒果片 罐装零食'
property_key = '规格'
property_value = '净重130g/罐 彩色标签'
price = 1800
market_price = 2500
banner_img_number = 3
detail_img_number = 11
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
