# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common import utils
from rest_framework import views
from .response import ApiJsonResponse
from .weixin import WXPayment

class Cart(views.APIView):
    
    def get(self, request):
        res = {
            'cart_info': {
                'sku_list': [
                    {
                        'sku_id': 1,
                        'brand': 'uptoyou',
                        'name': '内衣套装UP圣诞节礼物情趣内衣红色精致无钢圈可爱性感蕾丝内裤',
                        'count': 2, 
                        'price': 17.00, 
                        'image': utils.generate_image_url('20171224144042-4-1_dmjbs0_dmjbs0'),
                        'selected': 1
                    }
                ],
                'total_amount': 0.01
            }
        }
        return ApiJsonResponse(res)


