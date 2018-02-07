# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import views

from common.services.goods import Goods 
from .decorators import check_token
from .response import ApiJsonResponse

class BuyNowSettlementView(views.APIView):

    @check_token
    def post(self, request):
        sku_id = request.data.get('sku_id')
        number = int(request.data.get('number', '1'))
        receiver = request.data.get('receiver', None)

        receiver = receiver
        goods_obj = Goods.fetch_by_sku(sku_id)
        sku_info = goods_obj.get_sku_info(sku_id)
        item = {
            "sku_id": int(sku_id),
            "thumbnail": sku_info['image_url'],
            "price": float(sku_info['price'] / 100.0), 
            "number": number,
            "name": sku_info["goods_name"], 
            "attrs": sku_info['property'].split(';') 
        }

        total_amount = sku_info['price'] * number 
        amount_payable = total_amount 
        item_list = [item]

        data = {
            'items': item_list, 
            'total_amount': str(float(total_amount / 100.0)),
            'postage': '包邮',
            'amount_payable': str(float(amount_payable / 100.0))
        }
        if receiver is not None:
            data['receiver'] = receiver
        
        print data
        return ApiJsonResponse(data)
