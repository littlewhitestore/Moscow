# *-* coding:utf-8 *-*

from .models import OrderItem as OrderItemModel

class OrderItem(object):
    def __init__(self, order_item_id, model_obj=None):
        self.order_item_id = order_item_id
        self.__model_obj = model_obj

    def __confirm_model_obj(self):
        if self.__model_obj is None:
            try:
                self.__model_obj = OrderItemModel.objects.get(pk=self.order_item_id)
            except OrderItemModel.DoesNotExist:
                pass

    @classmethod
    def get_order_item_list(cls, order_sn):
        order_item_model_list = OrderItemModel.objects.filter(order_sn=order_sn)
        order_item_list = map(lambda _m:cls(_m.pk, model_obj=_m), order_item_model_list)
        return order_item_list

    @classmethod
    def create(cls, order_sn, goods_id, sku_id,
            sku_name, market_price, sale_price,
            number):
        order_item_model = OrderItemModel.objects.create(
                order_sn=order_sn,
                goods_id=goods_id,
                sku_id=sku_id,
                sku_name=sku_name,
                market_price=market_price,
                sale_price=sale_price,
                number=number)

        return cls(order_item_model.pk, order_item_model)

    def get_basic_info(self):
        self.__confirm_model_obj()
        return {
            'goods_id': self.__model_obj.goods_id,
            'sku_id': self.__model_obj.sku_id,
            'number': self.__model_obj.number,
            'sku_name': self.__model_obj.sku_name,
            'market_price': self.__model_obj.market_price,
            'sale_price': self.__model_obj.sale_price
        }

