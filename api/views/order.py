# *-* coding:utf-8 *-*

from __future__ import unicode_literals

from common.services.settlement.buynow import BuyNowSettlementService
from common.services.order import Order
from common.services.mina.payment import MinaPayment

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

        order_trade = order.apply_trade()

        # 配置是否需要根据APPID更换
        trade_basic_info = order_trade.get_basic_info()
        order_basic_info = order.get_order_basic_info()
        mina_payment = MinaPayment('wxd4eae843e18ff7da',
                '510861ca183551e3a7fcbdc87573c00f', '1495032292', 'aWNhdGUgQXV0aG9yXR5Q0wwYDVQQDEwR')
        trade_no = trade_basic_info.get('trade_no')
        trade_amount = trade_basic_info.get('trade_amount')
        prepay_id = mina_payment.get_prepay_id(trade_no, 
                trade_amount,
                order_basic_info.get('order_sn'), 
                request.user_obj.openid,
                'https://www.xiaobaidiandev.com')
        mina_payment_params = mina_payment.get_js_api_parameter(prepay_id)

        return ApiJsonResponse(mina_payment_params)

class OrderListView(views.APIView):
    def __order_data(self, order):
        order_basic_info = order.get_order_basic_info()
        basic_data = {
            'order_id': order_basic_info.get('order_id'),
            'status_desc': order.get_status_text(),
            'order_sn': order_basic_info.get('order_sn'),      # 订单号
            'postage': order_basic_info.get('postage'),        # 邮费
            'amount_payable': order_basic_info.get('amount_payable'), # 订单金额
        }
        order_items = order.get_order_item_list()
        items = []
        for order_item in order_items:
            item_basic = order_item.get_basic_info()
            items.append({
                'thumbnail': '#TODO获取sku的缩略图',
                'product_name': item_basic.get('product_name'),
                'number': item_basic.get('number'),
                'attrs': ['颜色:卡其色', '尺寸: XL'],
                'sale_price': item_basic.get('sale_price')
            })
        basic_data['items'] = items
        return basic_data

    @check_session
    def get(self, request):
        offset = request.data.get('offset', 0)
        count = request.data.get('count', 10)

        order_list = Order.get_order_list(1, offset, count)
        order_data = map(lambda _o: self.__order_data(_o), order_list)
        return ApiJsonResponse(order_data)

class OrderDetailView(views.APIView):
    def __order_data(self, order):
        order_basic_info = order.get_order_basic_info()
        basic_data = {
            'order_id': order_basic_info.get('order_id'),
            'status_desc': order.get_status_text(),
            'order_sn': order_basic_info.get('order_sn'),      # 订单号
            'postage': order_basic_info.get('postage'),        # 邮费
            'amount_payable': order_basic_info.get('amount_payable'), # 订单金额
        }
        order_items = order.get_order_item_list()
        items = []
        for order_item in order_items:
            item_basic = order_item.get_basic_info()
            items.append({
                'thumbnail': '#TODO获取sku的缩略图',
                'product_name': item_basic.get('product_name'),
                'number': item_basic.get('number'),
                'attrs': ['颜色:卡其色', '尺寸: XL'],
                'sale_price': item_basic.get('sale_price')
            })
        basic_data['items'] = items
        receiver = order.get_receiver()
        if receiver:
            receiver_basic = receiver.get_basic_info()
            basic_data['receiver'] = {
                'name': receiver_basic.get('name'),
                'mobile': receiver_basic.get('mobile'),
                'address': ' '.join([
                    receiver_basic.get('province'),
                    receiver_basic.get('city'),
                    receiver_basic.get('district'),
                    receiver_basic.get('address'),
                ])
            }
        return basic_data

    @check_session
    def get(self, request, order_id):
        order = Order(order_id)
        data = self.__order_data(order)
        return ApiJsonResponse(data)
