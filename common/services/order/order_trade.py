# *-* coding:utf-8 *-*
import datetime 
import random
from .models import OrderTradeModel

class TradeStatus(object):
    SUCCESS = 1

class OrderTrade(object):
    def __init__(self, pk, model_obj=None):
        self.pk = pk
        self.__model_obj = model_obj

    @classmethod
    def create(cls, order_id, order_sn, trade_amount):
        #TODO 当前逻辑可能生成重复交易号
        prefix = datetime.datetime.now().strftime("%Y%m%d")
        random_no = str(random.randint(1000000000, 9999999999))
        trade_no = "%s%s" % (prefix, random_no)
        order_trade_model = OrderTradeModel.objects.create(
            order_id=order_id,
            order_sn=order_sn,
            trade_no=trade_no,
            trade_amount=trade_amount
        )
        return cls(order_trade_model.pk, order_trade_model)

    @classmethod
    def from_trade_no(cls, trade_no):
        try:
            order_trade_model = OrderTradeModel.objects.get(
                    trade_no=trade_no)
            return cls(order_trade_model.pk, order_trade_model)
        except OrderTradeModel.DoesNotExist:
            return None

    def __confirm_model_obj(self):
        if self.__model_obj is None:
            try:
                self.__model_obj = OrderTradeModel.objects.get(
                        pk=self.pk)
            except OrderTradeModel.DoesNotExist:
                pass

    def get_basic_info(self):
        self.__confirm_model_obj()
        return {
            'trade_no': self.__model_obj.trade_no,
            'trade_amount': self.__model_obj.trade_amount,
        }

    def set_success(self):
        self.__confirm_model_obj()
        if self.__model_obj:
            self.__model_obj.trade_status = TradeStatus.SUCCESS
            self.__model_obj.save()

