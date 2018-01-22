# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from common.services.settlement.buynow import BuyNowSettlementService
from django.views import View
from rest_framework import views

from .decorators import check_session
from .response import ApiJsonResponse

class Product(object):
    product_id = 100000
    goods_id = 100001
    name = '黑色毛衣'
    market_price = 200
    price = 100

class BuyNowSettlementView(views.APIView):

    def __item_data(self, item):
        return {
            'name': item.product.name,
            'attrs': [
                '颜色:卡其色',
                '尺码:XL'
            ],
            'price': str(item.product.price), # item.price
            'thumbnail': '', # 获取sku的缩略图
            'number': item.number
        }

    @check_session
    def post(self, request):
        product_id = request.data.get('product_id')
        number = int(request.data.get('number', '1'))
        receiver = request.data.get('receiver', None)

        # 通过product_id获取product信息
        product = Product()

        service = BuyNowSettlementService(
                product, number, receiver)
        check_list = service.settlement()
        data = {
            'items': [self.__item_data(i) for i in check_list.product_list],
            'total_amount': str(check_list.total_amount),
            'postage': '包邮',
            'amount_payable': str(check_list.amount_payable)
        }
        if check_list.receiver is not None:
            data['receiver'] = check_list.receiver

        return ApiJsonResponse(data)
