# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views import View 
from common import utils
from .weixin import WXPayment

class Cart(View):
    
    def get(self, request):
        res = {
            'cart_info': {
                'product_list': [
                    {
                        'product_id': 1,
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
        return JsonResponse(res)


class Settlement(View):
    
    def get(self, request):
        out_trade_no = WXPayment.generate_test_out_trade_no()
        
        payment_obj = WXPayment(out_trade_no)
        prepay_id = payment_obj.get_prepay_id(
            1, 
            'test_xiaobaidian_pay', 
            'ooE4V0QzwSVR4AekmJI4b8nqLFi0',
            '127.0.0.1'
        )
        print prepay_id 

        res = {
            'cart_info': {
                'product_list': [
                    {
                        'product_id': 1,
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
        return JsonResponse(res)
