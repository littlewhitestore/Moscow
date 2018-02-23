# *-* coding:utf-8 *-*
from common.services.goods import Goods
from .models import PintuanModel
from .order import Order
from .snowflake import sn
import datetime

class PintuanStatus(object):
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

class Pintuan(object):
    
    def __init__(self, pintuan_id, model_obj=None):
        self.__pintuan_id = int(pintuan_id)
        self.__model_obj = model_obj

    def __confirm_pintuan_model(self):
        if self.__model_obj == None:
            self.__model_obj = PintuanModel.objects.get(pk=self.__pintuan_id)

    @property
    def id(self):
        return self.__pintuan_id
    
    @property
    def start_order_id(self):
        self.__confirm_pintuan_model()
        return self.__model_obj.start_order_id


    @classmethod
    def create(cls, entry, user_id, receiver, sku_id, number, price, order_total_amount, order_amount_payable): 
        finish_time = datetime.datetime.now() + datetime.timedelta(hours=72)
        pintuan_model_obj = PintuanModel.objects.create(
            pintuan_sn='19' + str(sn()),
            sku_id=sku_id,
            price=price,
            start_user_id=user_id,
            pintuan_status=PintuanStatus.CREATED,
            finish_time=finish_time
        )
        
        item_list = [{'sku_id': sku_id, 'number': number}] 
        order_obj = Order.create(
            entry=entry, 
            user_id=user_id,
            receiver=receiver,
            item_list=item_list, 
            total_amount=order_total_amount,
            amount_payable=order_amount_payable,
            pintuan_id=pintuan_model_obj.id
        )

        result = {
            'pintuan_obj': cls(pintuan_model_obj.id, pintuan_model_obj), 
            'start_order_obj': order_obj
        }
        return result
    
    @property
    def success_order_number(self):
        return 0

    
    @property
    def is_not_finished(self):
        self.__confirm_pintuan_model()
        if self.success_order_number > self.__model_obj.success_target:
            return False
        if datetime.datetime.now() > self.__model_obj.finish_time:
            return False 
        return True 
    
    @property
    def pintuan_price(self):
        self.__confirm_pintuan_model()
        return self.__model_obj.price
    
    def join(self, user_id, receiver, order_total_amount, order_amount_payable):
        self.__confirm_pintuan_model()
        item_list = [{'sku_id': self.__model_obj.sku_id, 'number': 1}] 
         
        order_obj = Order.create(
            entry=entry, 
            user_id=user_id,
            receiver=receiver,
            item_list=item_list, 
            total_amount=order_total_amount,
            amount_payable=order_amount_payable,
            pintuan_id=self.__model_obj.id
        )

        return order_obj 
