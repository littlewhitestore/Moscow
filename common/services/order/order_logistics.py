# *-* coding:utf-8 *-*
import json
import requests
from .models import OrderLogisticsModel
from .models import ExpressCompany

class OrderLogistics(object):
    def __init__(self, pk, model_obj=None):
        self.pk = pk
        self.__model_obj = model_obj

    def __confirm_model_obj(self):
        if self.__model_obj is None:
            try:
                self.__model_obj = OrderLogisticsModel.objects.get(pk=self.pk)
            except OrderLogisticsModel.DoesNotExist:
                pass

    @classmethod
    def create(cls, order_id, order_sn, com, nu):
        model_obj = OrderLogisticsModel.objects.create(
                order_id=order_id,
                order_sn=order_sn,
                com=com,
                nu=nu)
        return cls(model_obj.pk, model_obj=model_obj)

    @classmethod
    def get_order_logistics(cls, order_sn):
        try:
            model_obj = OrderLogisticsModel.objects.get(order_sn=order_sn)
            return cls(model_obj.pk, model_obj=model_obj)
        except OrderLogisticsModel.DoesNotExist:
            return None

    def get_basic_info(self):
        self.__confirm_model_obj()
        return {
            'com': self.__model_obj.com,
            'com_name': ExpressCompany.get(self.__model_obj.com, '未知'),
            'nu': self.__model_obj.nu,
            'data': self.__model_obj.data
        }

    def refresh(self, data):
        self.__confirm_model_obj()
        self.__model_obj.data = data
        self.__model_obj.save()

    def subscribe(self):
        self.__confirm_model_obj()
        __body = {
            "company": self.__model_obj.com,
            "number": self.__model_obj.nu,
            "key": "VBTKOCdI7267",
            "parameters": {
                "callbackurl": 'https://www.xiaobaidiandev.com/api/orders/%s/logistics' % self.__model_obj.order_sn
            }
        }
        data = {
            "schema": "json",
            "param": json.dumps(__body)
        }
        r = requests.post("http://www.kuaidi100.com/poll", data=data)
