# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse 
from django.views import View 



class HelloWorld(View):
    
    def get(self, request):
        return HttpResponse("hello world!")


class Home(View):
    
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
        return JsonResponse(res)
