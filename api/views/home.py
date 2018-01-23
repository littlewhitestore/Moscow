# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from .decorators import check_session 
from .response import ApiJsonResponse

class HelloWorld(View):
    
    def get(self, request):
        res = {
            'text': 'hello world!'
        }
        return ApiJsonResponse(res)

class Home(View):
    
    @check_session
    def get(self, request):
        res = {
            "banner_img_list": [
                {
                    "url": "../goods/detail?goodsId=1000",
                    "img": "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/banner1.jpeg",
                },
                {
                    "url": "../goods/detail?goodsId=1000",
                    "img": "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/banner2.jpeg"
                }
            ],
            "goods_list": [
                {
                    "goods_id": 1000,
                    "goods_name": "爆款毛衣",
                    "goods_price": 99.99,
                    "market_price": 129.99,
                    "goods_img": "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/test_goods_1.jpeg",
                    "url": "../goods/detail?goodsId=1000",
                },
                {
                    "goods_id": 1000,
                    "goods_name": "爆款毛衣",
                    "goods_price": 99.99,
                    "market_price": 129.99,
                    "goods_img": "http://xiaobaidian-img-001-1255633922.picgz.myqcloud.com/test_goods_1.jpeg",
                    "url": "../goods/detail?goodsId=1000",
                }
            ]
        }
        return ApiJsonResponse(res)

