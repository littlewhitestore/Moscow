# *-* coding:utf-8 *-*
from .models import Order as OrderModel
from .models import OrderReceiver as OrderReceiverModel


class OrderReceiver(object):
    def __init__(self, pk, order_receiver_model_obj=None):
        self.pk = pk
        self.__model_obj = order_receiver_model_obj

    @classmethod
    def get_order_receiver(cls, order_sn):
        try:
            recevier_model = OrderReceiverModel.objects.get(
                    order_sn=order_sn)
            return cls(recevier_model.pk, recevier_model)
        except OrderReceiverModel.DoesNotExist:
            return None

    def __confirm_model_obj(self):
        if self.__model_obj is None:
            try:
                self.__model_obj = OrderReceiverModel.objects.get(
                        pk=self.pk)
            except OrderReceiverModel.DoesNotExist:
                pass

    @classmethod
    def create(cls, order_sn, name, province, city, district, address, mobile, zipcode=''):
        order_receiver_model = OrderReceiverModel.objects.create(
                order_sn=order_sn,
                name=name,
                province=province,
                city=city,
                district=district,
                address=address,
                mobile=mobile,
                zipcode=zipcode)

        return cls(order_receiver_model.pk, order_receiver_model)

    def get_basic_info(self):
        self.__confirm_model_obj()
        return {
            'name': self.__model_obj.name,
            'province': self.__model_obj.province,
            'city': self.__model_obj.city,
            'district': self.__model_obj.district,
            'address': self.__model_obj.address,
            'mobile': self.__model_obj.mobile
        }

