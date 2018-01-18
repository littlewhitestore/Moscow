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
            'product_data_list': [
                {
                    'id': 1,
                    'name': '测试商品',
                    'price_yh': 20.00, 
                    'price': 18.88, 
                    'is_show': 1,
                    'shiyong': 100
                }
            ]
        }
        return ApiJsonResponse(res)

