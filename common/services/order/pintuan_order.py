# *-* coding:utf-8 *-*
from common.services.goods import Goods
from .models import PintuanOrderModel
from .order import Order
import datetime

class PintuanOrderStatus(object):
    CREATED = 1
    SUCCESS = 2
    FAILED = 3

    @classmethod
    def dict(cls):
        return {
            cls.CREATED: "已开团",
            cls.SUCCESS: "拼团成功",
            cls.FAILED: "拼团失败",
        }

class PintuanOrder(object):
    
    def __init__(self, pintuan_order_id, model_obj=None):
        self.__pintuan_order_id = int(pintuan_order_id)
        self.__model_obj = model_obj

    def __confirm_pintuan_order_model(self):
        if self.__model_obj == None:
            self.__model_obj = PintuanOrderModel.objects.get(pk=self.__pintuan_order_id)

    @property
    def id(self):
        return self.__pintuan_order_id
    
    @property
    def start_order_id(self):
        self.__confirm_pintuan_order_model()
        return self.__model_obj.start_order_id


    @classmethod
    def create(cls, entry, user_id, receiver, sku_id, price, order_total_amount, order_amount_payable): 
        
        finish_time = datetime.datetime.now() + datetime.timedelta(hours=24)
        pintuan_order_model_obj = PintuanOrderModel.objects.create(
            sku_id=sku_id,
            price=price,
            start_user_id=user_id,
            pintuan_order_status=PintuanOrderStatus.CREATED,
            finish_time=finish_time
        )
        
        item_list = {['sku_id': sku_id, 'number': 1]} 
        order_obj = Order.create(
            entry=entry, 
            user_id=user_id,
            receiver=receiver,
            item_lis=item_list, 
            total_amount=order_total_amount,
            amount_payable=order_amount_payable,
            pintuan_id=pintuan_order_model_obj.id
        )

        result = {
            'pintuan_order_obj': cls(pintuan_order_model.id, pintuan_order_model), 
            'start_order_obj': order_obj
        }
        return result

