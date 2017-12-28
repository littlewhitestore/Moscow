# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse 
from django.views import View 

from .cart import *


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


def generate_image_url(image_key):
    return "https://www.xiaobaidian.cn/static/img/%s.jpg"%image_key


class GoodsDetail(View):
    
    def get(self, request, goods_id):
        res = {
            'goods_info': {
                'id': 1,
                'brand': 'uptoyou',
                'name': '内衣套装UP圣诞节礼物情趣内衣红色精致无钢圈可爱性感蕾丝内裤',
                'banner_list': [
                    generate_image_url('007125fd09tb2'),
                    generate_image_url('007268421btb2ud_xa___898341892'),
                    generate_image_url('00733905e5tb25abxa___898341892'),
                    generate_image_url('0074a7eb21tb20wgxa___898341892'),
                    generate_image_url('007631b580tb221vxa___898341892')
                ],
                'detail_image_list': [
                    generate_image_url('20171224144042-4-1_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-2_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-4_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-5_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-6_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-7_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-8_dmjbs0'),
                    generate_image_url('20171224144042-4-9_dmjbs0'),
                    generate_image_url('20171224144042-4-10_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-11_dmjbs0'),
                    generate_image_url('20171224144042-4-12_dmjbs0'),
                    generate_image_url('20171224144042-4-13_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-14_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-15_dmjbs0'),
                    generate_image_url('20171224144042-4-16_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-17_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-18_dmjbs0_dmjbs0'),
                    generate_image_url('20171224144042-4-19_dmjbs0'),
                    generate_image_url('20171224144042-4-20_dmjbs0'),
                ]
            }
        }
        return JsonResponse(res)


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
                        'image': generate_image_url('20171224144042-4-1_dmjbs0_dmjbs0'),
                    }
                ]
            }
        }
        return JsonResponse(res)
