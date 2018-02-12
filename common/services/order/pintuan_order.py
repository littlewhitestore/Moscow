# *-* coding:utf-8 *-*
from common.services.goods import Goods
from .models import PintuanOrderModel
from .order import Order

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
    def create(cls, sku_id, price, user_id, receiver):
        item_list = [{
            'sku_id': sku_id, 
            'number': number
        }]
        total_amount = price
        amount_payable = price
        order_obj = Order.create(user_id, receiver, item_list, total_amount, amount_payable)

        pintuan_order_model = PintuanOrderModel.objects.create(
            sku_id=sku_id,
            price=price,
            start_order_id=order_obj.id,
            pintuan_order_status=PintuanOrderStatus.CREATED
        )


