# *-* coding:utf-8 *-*

from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
import xmltodict

from common.services.mina.payment import MinaPayment
from common.services.order import Order
from common.services.settlement.buynow import BuyNowSettlementService
from .decorators import check_token
from .response import ApiJsonResponse

class Product(object):
    product_id = 100000
    goods_id = 100001
    name = '黑色毛衣'
    market_price = 200
    price = 100

class BuyNowOrderView(views.APIView):

    @check_token
    def post(self, request):
        product_id = request.data.get('product_id')
        number = request.data.get('number', 1)
        receiver = request.data.get('receiver', None)

        product = Product()
        user_obj = request.user_obj

        settlement_service = BuyNowSettlementService(
                product, number, receiver)
        check_list = settlement_service.settlement()

        order = Order.create(user_obj.id, check_list)

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
                'https://www.xiaobaidiandev.com/api/orders/{order_id}/payment'.format(
                    order_id=order_basic_info.get('order_id'))
            )
        mina_payment_params = mina_payment.get_js_api_parameter(prepay_id)

        #data = {
        #    'order_id': order_basic_info.get('order_id'),
        #    'mina_payment': mina_payment_params
        #}

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

    @check_token
    def get(self, request):
        offset = request.data.get('offset', 0)
        count = request.data.get('count', 10)
        user_obj = request.user_obj

        order_list = Order.get_order_list(user_obj.id, offset, count)
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

    @check_token
    def get(self, request, order_id):
        order = Order(order_id)
        data = self.__order_data(order)
        return ApiJsonResponse(data)

class WeixinResponse(object):
    def __init__(self, code='SUCCESS', msg='OK'):
        self.__code = code
        self.__msg = msg

    def __str__(self):
        return "<xml><return_code><![CDATA[%s]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>" % (self.__code, self.__msg)

@csrf_exempt
def weixin_pay_cb(request, order_id):
    cb_data = xmltodict.parse(request.body).get('xml')
    return_code = cb_data.get('return_code')
    out_trade_no = cb_data.get('out_trade_no')
    total_fee = cb_data.get('total_fee')
    result_code = cb_data.get('result_code')
    transaction_id = cb_data.get('transaction_id')
    trade_type = cb_data.get('trade_type')
    fee_type = cb_data.get('fee_type')
    appid = cb_data.get("appid")
    mch_id = cb_data.get("mch_id")

    if return_code == "SUCCESS":
        order = Order(order_id)
        order.pay(out_trade_no)
        return HttpResponse(WeixinResponse())
    return HttpResponse(WeixinResponse(code="FAIL", msg="WEIXIN FAIL"))
