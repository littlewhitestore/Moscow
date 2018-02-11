# *-* coding:utf-8 *-*
from __future__ import unicode_literals
from django.conf import settings

from common.services.goods import Goods 
from common.services.order import Order
from minapp_payment import MinappPayment

class SettlementManager(object):
    
    def __init__(self, user_id, user_openid):
        self.__user_id = user_id
        self.__user_openid = user_openid

    
    def buynow_settlement(self, sku_id, number):
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
        settlement_info = {
            'total_amount': sku_info['price'] * number,
            'amount_payable': sku_info['price'] * number, 
            'item_list': [item]
        }
        return settlement_info 


    def buynow_checkout(self, entry, sku_id, number, receiver):
        
        settlement_info = self.buynow_settlement(sku_id, number)

        order = Order.create(
            user_id=self.__user_id,
            receiver=receiver,
            item_list=settlement_info['item_list'],
            total_amount=settlement_info['total_amount'],
            amount_payable=settlement_info['amount_payable']
        )
        order_trade = order.apply_trade()

        trade_basic_info = order_trade.get_basic_info()
        order_basic_info = order.get_order_basic_info()
        mina_payment = MinappPayment(
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
            order_basic_info['order_sn'],
            self.__user_openid,
            'https://www.xiaobaidiandev.com/api/orders/{order_id}/pay/success'.format(
                order_id=order_basic_info['order_id']
            )
        )
        mina_payment_params = mina_payment.get_js_api_parameter(prepay_id)

        checkout_info = {
            'order_id': order_basic_info.get('order_id'),
            'mina_payment': mina_payment_params
        }

        return checkout_info 

