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


class GoodsUpload(views.APIView):

    def post(self, request):
        banner_images = request.data.get('banner_images')
        detail_images = request.data.get('detail_images')
        name = request.data.get('name')
        supply_source = request.data.get('supply_source')
        supply_item_id = request.data.get('supply_item_id')
        price = request.data.get('price')
        market_price = request.data.get('market_price')
        
        banner_image_list = banner_images.split(';')
        detail_image_list = detail_images.split(';')
        
        goods_obj = Goods.create(
            name=name,
            supply_source=supply_source,
            supply_item_id=supply_item_id,
            price=price,
            market_price=market_price,
            status=1,
            banner_image_list=banner_image_list,
            detail_image_list=detail_image_list
        )

        
        res = {
            'goods_id': goods_obj.id 
        }
        return ApiJsonResponse(res)

class GoodsSkuUpload(views.APIView):

    def post(self, request, goods_id):
        property_vector_str = request.data.get('property_vector_str')
        image_url = request.data.get('image_url')
        price = request.data.get('price')
        stock = request.data.get('stock', 1000)
        
        property_vector_list = property_vector_str.split('|')
        property_vector = []
        i = 0
        while (i < len(property_vector_list) and i < 4):
            property_vector.append({
                'key': property_vector_list[i], 
                'value': property_vector_list[i + 1], 
            })
            i += 2
        
        goods_obj = Goods(goods_id)
        sku_id = goods_obj.add_sku(
            image_url=image_url,
            property_vector=property_vector, 
            price=price,
            stock=stock
        )

        
        res = {
            'goods_id': goods_obj.id, 
            'sku_id': sku_id 
        }
        return ApiJsonResponse(res)
