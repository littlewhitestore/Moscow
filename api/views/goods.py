# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from common import utils
from .response import ApiJsonResponse

class GoodsDetail(View):

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

