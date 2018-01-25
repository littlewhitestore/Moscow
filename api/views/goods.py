# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common import utils
from common.services.goods import Goods
from rest_framework import views
from .response import ApiJsonResponse

class GoodsDetail(views.APIView):

    def get(self, request, goods_id):
        
        goods_obj = Goods(1)
        goods_info = goods_obj.read()
        
        res = {
            "goods_id": goods_info['id'],
            "goods_name": goods_info['name'], 
            "goods_price": goods_info['price'], 
            "market_price": goods_info['market_price'], 
            "banner_img_list": goods_info['banner_image_list'],
            "goods_detail_img_list": goods_info['detail_image_list'],
            "postage_desc": "免邮费",
            "services":[
                {"type": 1, "desc":"正品保障"},
                {"type": 2, "desc":"发货&售后"},
                {"type": 3, "desc":"七天退换"}
            ],
        }
        return ApiJsonResponse(res)


class GoodsUpload(views.APIView):

    def post(self, request):
        banner_images = request.data.get('banner_images')
        detail_images = request.data.get('detail_images')
        name = request.data.get('name')
        taobao_id = request.data.get('taobao_id')
        price = request.data.get('price')
        market_price = request.data.get('market_price')
        
        banner_image_list = banner_images.split(';')
        detail_image_list = detail_images.split(';')
        
        goods_obj = Goods.create(
            name=name,
            taobao_id=taobao_id,
            price=price,
            market_price=market_price,
            status=0,
            banner_image_list=banner_image_list,
            detail_image_list=detail_image_list
        )

        
        res = {
            'goods_id': goods_obj.id 
        }
        return ApiJsonResponse(res)
