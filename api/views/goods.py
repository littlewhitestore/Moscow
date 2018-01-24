# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common import utils
from common.services.goods import Goods
from rest_framework import views
from .response import ApiJsonResponse

class GoodsDetail(views.APIView):

    def get(self, request, goods_id):
        res = {
            "goods_id": 1234,
            "goods_name": "台湾木匠手作恐龙考古侏罗纪化石巧克力礼盒新年礼物 现货顺丰",
            "goods_price": 99.99,
            "market_price": 129.99,
            "banner_img_list":[
                "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/banner1.jpeg",
                "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/banner2.jpeg"
            ], 
            "postage_desc": "免邮费",
            "services":[
                {"type": 1, "desc":"正品保障"},
                {"type": 2, "desc":"发货&售后"},
                {"type": 3, "desc":"七天退换"}
            ],
            "goods_detail_img_list":[
                "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/test_goods_5.jpeg",
                "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/test_goods_6.jpeg",
                "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/test_goods_7.jpeg"
            ]
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
        
        print taobao_id
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
