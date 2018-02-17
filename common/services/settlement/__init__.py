# *-* coding:utf-8 *-*
from __future__ import unicode_literals
from django.conf import settings

from common.services.goods import Goods 
from common.services.order import Order, Pintuan
from common.services.payment import MinappPayment

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
            "price": sku_info['price'], 
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
            entry=entry,
            user_id=self.__user_id,
            receiver=receiver,
            item_list=settlement_info['item_list'],
            total_amount=settlement_info['total_amount'],
            amount_payable=settlement_info['amount_payable']
        )
        minapp_payment_params = order.checkout(self.__user_openid) 

        checkout_info = {
            'order_id': order.id, 
            'mina_payment': minapp_payment_params
        }

        return checkout_info 

    def pintuan_settlement(self, sku_id):
        goods_obj = Goods.fetch_by_sku(sku_id)
        sku_info = goods_obj.get_sku_info(sku_id)
        item = {
            "sku_id": int(sku_id),
            "thumbnail": sku_info['image_url'],
            "price": sku_info['price'], 
            "number": 1,
            "name": sku_info["goods_name"], 
            "attrs": sku_info['property'].split(';') 
        }
        settlement_info = {
            'total_amount': sku_info['price'],
            'amount_payable': sku_info['price'], 
            'item_list': [item]
        }
        return settlement_info 

    
    def pintuan_checkout(self, entry, sku_id, number, receiver):
        settlement_info = self.pintuan_settlement(sku_id)
        
        result = PintuanOrder.create(
            entry=entry,
            user_id=self.__user_id,
            receiver=receiver,
            sku_id=sku_id, 
            price=settlement_info['price'],
            order_total_amount=settlement_info['total_amount'],
            order_amount_payable=settlement_info['amount_payable']
        )
        pintuan_obj = result['pintuan_obj']
        start_order_obj = result['start_order_obj']
        minapp_payment_params = start_order_obj.checkout(self.__user_openid) 

        checkout_info = {
            'order_id': start_order_obj.id, 
            'mina_payment': minapp_payment_params
        }

        return checkout_info 
