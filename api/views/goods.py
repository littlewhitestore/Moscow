# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common import utils
from common.services.goods import Goods
from rest_framework import views
from .response import ApiJsonResponse

class GoodsDetail(views.APIView):

    def get(self, request, goods_id):
        
        goods_obj = Goods(goods_id)
        goods_info = goods_obj.read()
        sku_list = goods_obj.fetch_sku_all()
        
        res = {
            "goods_id": goods_info['id'],
            "goods_name": goods_info['name'], 
            "goods_price": float(goods_info['price']) / 100.0, 
            "market_price": float(goods_info['market_price']) / 100.0, 
            "banner_img_list": goods_info['banner_image_list'],
            "goods_detail_img_list": goods_info['detail_image_list'],
            "postage_desc": "免邮费",
            "services":[
                {"type": 1, "desc":"正品保障"},
                {"type": 2, "desc":"发货&售后"},
                {"type": 3, "desc":"七天退换"}
            ],
            "sku_list": [],
            "property_vector": []
        }
        
        first = True
        for sku in sku_list:
            item = {
                "sku_id": sku['id'],
                "price": float(sku['price']) / 100.0, 
                "property_value_vector": [], 
                "img": sku['image_url'], 
                "stock": sku['stock'], 
            }
            
            i = 0
            for kv in sku["property_vector"]:
                if first == True:
                    res["property_vector"].append({
                        "key": kv["key"],
                        "values": []
                    })
                item["property_value_vector"].append(kv['value'])
                if not kv["value"] in res["property_vector"][i]["values"]:
                    res["property_vector"][i]["values"].append(kv['value'])
                i += 1
            
            res["sku_list"].append(item)
            first = False
        
        return ApiJsonResponse(res)


