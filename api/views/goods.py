# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View 
from common import utils
from .response import ApiJsonResponse

class GoodsDetail(View):
    
    def get(self, request, goods_id):
        res = {
            'goods_info': {
                'id': 1,
                'brand': 'uptoyou',
                'name': '内衣套装UP圣诞节礼物情趣内衣红色精致无钢圈可爱性感蕾丝内裤',
                'banner_list': [
                    utils.utils.generate_image_url('007125fd09tb2'),
                    utils.generate_image_url('007268421btb2ud_xa___898341892'),
                    utils.generate_image_url('00733905e5tb25abxa___898341892'),
                    utils.generate_image_url('0074a7eb21tb20wgxa___898341892'),
                    utils.generate_image_url('007631b580tb221vxa___898341892')
                ],
                'detail_image_list': [
                    utils.generate_image_url('20171224144042-4-1_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-2_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-4_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-5_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-6_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-7_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-8_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-9_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-10_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-11_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-12_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-13_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-14_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-15_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-16_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-17_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-18_dmjbs0_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-19_dmjbs0'),
                    utils.generate_image_url('20171224144042-4-20_dmjbs0'),
                ]
            }
        }
        return ApiJsonResponse(res)

