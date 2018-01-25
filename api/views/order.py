# *-* coding:utf-8 *-*

from __future__ import unicode_literals

from common.services.settlement.buynow import BuyNowSettlementService
from common.services.order import Order

from rest_framework import views

from .decorators import check_session
from .response import ApiJsonResponse

class Product(object):
    product_id = 100000
    goods_id = 100001
    name = '黑色毛衣'
    market_price = 200
    price = 100

class User(object):
    id = 1

class BuyNowOrderView(views.APIView):

    @check_session
    def post(self, request):
        product_id = request.data.get('product_id')
        number = request.data.get('number', 1)
        receiver = request.data.get('receiver', None)

        product = Product()
        user = User()

        settlement_service = BuyNowSettlementService(
                product, number, receiver)
        check_list = settlement_service.settlement()

        order = Order.create(user.id, check_list)

        return ApiJsonResponse()
