# -*- coding: utf-8 -*- from __future__ import unicode_literals
from rest_framework import views

from common.services.goods import Goods 
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
        
        offset = int(request.GET.get('offset', '0'))
        count = int(request.GET.get('count', '20'))
        
        res = {
            "banner_img_list": [],
            "goods_list": []
        }
        
        goods_obj_list = Goods.fetch_recommend_goods(offset, count)
        for goods_obj in goods_obj_list:
            goods_info = goods_obj.read()
            
            goods_img = '' 
            if len(goods_info['banner_image_list']) > 0:
                goods_img = goods_info['banner_image_list'][0]
            
            res['goods_list'].append({
                "goods_id": goods_info['id'],
                "goods_name": goods_info['name'], 
                "goods_price": float(goods_info['price']) / 100.0, 
                "market_price": float(goods_info['market_price']) / 100.0, 
                "goods_img": goods_img,
                "url": "../goods/detail?goodsId=%d"%goods_obj.id,
            })
            
        
        if offset == 0:
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
