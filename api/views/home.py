# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import views

from common.services.home import HomeBanner
from .decorators import check_token
from .response import ApiJsonResponse

class HelloWorld(views.APIView):
    
    def get(self, request):
        res = {
            'text': 'hello world!'
        }
        return ApiJsonResponse(res)

class Home(views.APIView):
    
    @check_token
    def get(self, request):
        res = {
            "banner_img_list": [],
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
        home_banner_list = HomeBanner.fetch_all()
        for banner in home_banner_list:
            res['banner_img_list'].append({
                'url': '',
                'img': banner['image'] 
            })
        return ApiJsonResponse(res)


class HomeBannerUpload(views.APIView):

    def post(self, request):
        image = request.data.get('image')
        refer = request.data.get('refer')
        sort = int(request.data.get('sort', 1))
        

        HomeBanner.add(image, refer, sort)
        
        res = {}
        return ApiJsonResponse(res)
