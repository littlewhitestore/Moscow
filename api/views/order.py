# *-* coding:utf-8 *-*

from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
import xmltodict

from common.services.goods import Goods 
from common.services.mina.payment import MinaPayment
from common.services.order import Order
from .decorators import check_token, login_required
from .response import ApiJsonResponse, ApiResponseStatusCode

import json

class BuyNowOrderView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        sku_id = request.data.get('sku_id')
        number = int(request.data.get('number', '1'))
        receiver = request.data.get('receiver', None)
        
        receiver = receiver
        item_list = [{
            'sku_id': int(sku_id),
            'number': number 
        }]
        goods_obj = Goods.fetch_by_sku(sku_id)
        sku_info = goods_obj.get_sku_info(sku_id)
        total_amount = sku_info['price'] * number 
        amount_payable = total_amount 

        order = Order.create(
            user_id=request.user_obj.id, 
            receiver=receiver,
            item_list=item_list,
            total_amount=total_amount,
            amount_payable=amount_payable
        )
        order_trade = order.apply_trade()

        # 配置是否需要根据APPID更换
        entry = request.entry
        trade_basic_info = order_trade.get_basic_info()
        order_basic_info = order.get_order_basic_info()
        mina_payment = MinaPayment(
            settings.ENTRY_CONFIG[entry]['WECHAT_APP_ID'],
            settings.ENTRY_CONFIG[entry]['WECHAT_APP_SECRET'],
            settings.ENTRY_CONFIG[entry]['WXPAY_MCH_ID'],
            settings.ENTRY_CONFIG[entry]['WXPAY_API_KEY'],
        )
        trade_no = trade_basic_info.get('trade_no')
        trade_amount = trade_basic_info.get('trade_amount')
        prepay_id = mina_payment.get_prepay_id(
            trade_no,
            trade_amount,
            order_basic_info.get('order_sn'),
            request.user_obj.openid,
            'https://www.xiaobaidiandev.com/api/orders/{order_id}/pay/success'.format( order_id=order_basic_info.get('order_id'))
        )
        mina_payment_params = mina_payment.get_js_api_parameter(prepay_id)

        data = {
            'order_id': order_basic_info.get('order_id'),
            'mina_payment': mina_payment_params
        }

        return ApiJsonResponse(data)

class OrderListView(views.APIView):
    
    
    def __order_data(self, order):
        order_basic_info = order.get_order_basic_info()
        basic_data = {
            'order_id': order_basic_info.get('order_id'),
            'status_desc': order.get_status_text(),
            'order_sn': order_basic_info.get('order_sn'),      # 订单号
            'postage': order_basic_info.get('postage'),        # 邮费
            'amount_payable': float(order_basic_info.get('amount_payable')) / 100.0, # 订单金额
        }
        order_items = order.get_order_item_list()
        items = []
        for order_item in order_items:
            item_basic = order_item.get_basic_info()
            sku_id = item_basic['sku_id']
            goods_obj = Goods.fetch_by_sku(sku_id)
            sku_info = goods_obj.get_sku_info(sku_id)
            items.append({
                'thumbnail': sku_info['image_url'], 
                'sku_name': item_basic['goods_name'],
                'number': item_basic['number'],
                'attrs': item_basic['sku_property'], 
                'sale_price': float(item_basic['sale_price']) / 100.0
            })
        basic_data['items'] = items
        return basic_data

    @check_token
    def get(self, request):
        user_obj = request.user_obj
        if user_obj == None:
            return ApiJsonResponse({}, ApiResponseStatusCode.RELOGIN)

        offset = request.data.get('offset', 0)
        count = request.data.get('count', 10)
        order_list = Order.get_order_list(user_obj.id, offset, count)
        order_data = map(lambda _o: self.__order_data(_o), order_list)
        return ApiJsonResponse(order_data)

class OrderDetailView(views.APIView):
    def __order_data(self, order):
        order_basic_info = order.get_order_basic_info()
        basic_data = {
            'order_id': order_basic_info.get('order_id'),
            'user_id': order_basic_info.get('user_id'),
            'status_desc': order.get_status_text(),
            'order_sn': order_basic_info.get('order_sn'),      # 订单号
            'postage': order_basic_info.get('postage'),        # 邮费
            'amount_payable': float(order_basic_info.get('amount_payable')) / 100.0, # 订单金额
        }
        order_items = order.get_order_item_list()
        items = []
        for order_item in order_items:
            item_basic = order_item.get_basic_info()
            sku_id = item_basic['sku_id']
            goods_obj = Goods.fetch_by_sku(sku_id)
            sku_info = goods_obj.get_sku_info(sku_id)
            items.append({
                'thumbnail': sku_info['image_url'], 
                'sku_name': item_basic['goods_name'],
                'number': item_basic['number'],
                'attrs': item_basic['sku_property'], 
                'sale_price': float(item_basic['sale_price']) / 100.0
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
        logistics = order.get_logistics()
        if logistics:
            logistics_basic = logistics.get_basic_info()
            logistics_res = {
                'com': logistics_basic.get('com_name'),
                'nu': logistics_basic.get('nu'),
            }
            logistics_data = logistics_basic.get('data')
            if logistics_data:
                logistics_res['data'] = json.loads(logistics_data)
            basic_data['logistics'] = logistics_res

        return basic_data

    @check_token
    def get(self, request, order_id):
        user_obj = request.user_obj
        if user_obj == None:
            return ApiJsonResponse({}, ApiResponseStatusCode.RELOGIN)

        order = Order(order_id)
        data = self.__order_data(order)

        if data['user_id'] != user_obj.id:
            return ApiJsonResponse({}, ApiResponseStatusCode.ERROR, "WRONG USER")

        return ApiJsonResponse(data)

class WeixinResponse(object):
    def __init__(self, code='SUCCESS', msg='OK'):
        self.__code = code
        self.__msg = msg

    def __str__(self):
        return "<xml><return_code><![CDATA[%s]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>" % (self.__code, self.__msg)


class WeixinPayCallbackView(views.APIView):
    
    @csrf_exempt
    def post(self, request, order_id):
        callback_data = xmltodict.parse(request.body).get('xml')
        return_code = callback_data.get('return_code')
        out_trade_no = callback_data.get('out_trade_no')
        total_fee = callback_data.get('total_fee')
        result_code = callback_data.get('result_code')
        transaction_id = callback_data.get('transaction_id')
        trade_type = callback_data.get('trade_type')
        fee_type = callback_data.get('fee_type')
        appid = callback_data.get("appid")
        mch_id = callback_data.get("mch_id")
    
        if return_code == "SUCCESS":
            order = Order(order_id)
            order.pay(out_trade_no)
            return HttpResponse(WeixinResponse())
        return HttpResponse(WeixinResponse(code="FAIL", msg="WEIXIN FAIL"))

@csrf_exempt
def delivery(request, order_sn):
    data = json.loads(request.POST.get('param'))
    status = data.get('status', 'polling')
    message = data.get('message', '')
    last_result = data.get('lastResult')
    if last_result is not None:
        ischeck = True if last_result.get('ischeck') == "1" else False
        com = last_result.get('com')
        nu = last_result.get('nu')
        logistics_data = last_result.get('data')
        order = Order.get_order_by_sn(order_sn)
        if order:
            order.refresh_logistics(com, nu, json.dumps(logistics_data), is_check=ischeck)

    data = {
        "result": "true",
        "returnCode": "200",
        "message": "成功"
    }

    return JsonResponse(data)
