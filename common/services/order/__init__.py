# *-* coding:utf-8 *-*

from .models import Order as OrderModel
from .models import OrderItem as OrderItemModel
from .models import OrderReceiver as OrderReceiverModel

from .snowflake import sn

class Order(object):
    def __init__(self, order_id, model_obj=None):
        self.order_id = order_id
        self.__model_obj = model_obj
        self.__receiver = None
        self.__order_items = []

    @classmethod
    def get_order_list(cls, user_id, offset, count):
        qs = OrderModel.objects.filter(user_id)
        qs = qs[offset: offset + count]
        order_list = map(lambda _m:cls(_m.pk, model_obj=_m), qs)
        return order_list

    @classmethod
    def create(cls, user_id, check_list):
        '''
        创建订单

        参数:
        @param user_id 用户ID
        @param check_list 结算系统生成的结算清单
        '''
        total_amount = check_list.total_amount
        amount_payable = check_list.amount_payable
        postage = check_list.postage
        order_model = OrderModel.objects.create(
                order_sn='18' + str(sn()),
                user_id=user_id,
                total_amount=total_amount,
                amount_payable=amount_payable,
                postage=postage)
        order =  cls(order_model.pk, model_obj=order_model)
        for item in check_list.product_list:
            order.add_order_item(item.product.goods_id,
                    item.product.product_id,
                    item.product.name,
                    item.product.market_price,
                    item.product.price,
                    item.number)
        receiver = check_list.receiver
        order.set_receiver(receiver.get('name'),
                receiver.get('province'),
                receiver.get('city'),
                receiver.get('district'),
                receiver.get('address'),
                receiver.get('mobile'),
                receiver.get('zipcode', ''),
            )

        return order

    def __confirm_receiver(self):
        if self.__receiver is None:
            self.__confirm_order_model()
            self.__receiver = OrderReceiver.get_order_receiver(self.__model_obj.order_sn)

    def __confirm_order_model(self):
        if self.__model_obj is None:
            try:
                self.__model_obj = OrderModel.objects.get(pk=self.order_id)
            except OrderModel.DoesNotExist:
                pass

    def __confirm_order_item_list(self):
        if not self.__order_items:
            self.__confirm_order_model()
            self.__order_items = OrderItem.get_order_item_list(self.__model_obj.order_sn)

    def get_order_basic_info(self):
        self.__confirm_order_model()
        return {
            'order_id': self.__model_obj.pk,
            'order_sn': self.__model_obj.order_sn,
            'user_id': self.__model_obj.user_id,
            'total_amount': self.__model_obj.total_amount,
            'postage': self.__model_obj.postage,
            'amount_payable': self.__model_obj.amount_payable,
            'created_time': self.__model_obj.created_time,
            'order_status': self.__model_obj.order_status
        }

    def set_receiver(self, name, province, city, district, address, mobile, zipcode=''):
        '''
        设置订单的收件人
        '''
        self.__confirm_order_model()
        self.__receiver = OrderReceiver.create(
                self.__model_obj.order_sn,
                name,
                province,
                city,
                district,
                address,
                mobile,
                zipcode)

    def get_receiver(self):
        '''
        获取订单收件人信息
        '''
        self.__confirm_receiver()
        return self.__receiver

    def get_order_item_list(self):
        '''
        获取订单商品明细信息
        '''
        self.__confirm_order_item_list()
        return self.__order_items

    def add_order_item(self, goods_id, product_id, product_name,
            market_price,
            sale_price,
            number):
        self.__confirm_order_model()
        order_item = OrderItem.create(
                self.__model_obj.order_sn,
                goods_id,
                product_id,
                product_name,
                market_price,
                sale_price,
                number)

class OrderItem(object):
    def __init__(self, order_item_id, order_item_model_obj=None):
        self.order_item_id = order_item_id
        self.__model_obj = order_item_model_obj

    @classmethod
    def get_order_item_list(cls, order_sn):
        order_item_model_list = OrderItemModel.objects.filter(order_sn=order_sn)
        order_item_list = map(lambda _m:cls(_m.pk, model_obj=_m), order_item_model_list)
        return order_item_list

    @classmethod
    def create(cls, order_sn, goods_id, product_id,
            product_name, market_price, sale_price,
            number):
        order_item_model = OrderItemModel.objects.create(
                order_sn=order_sn,
                goods_id=goods_id,
                product_id=product_id,
                product_name=product_name,
                market_price=market_price,
                sale_price=sale_price,
                number=number)

        return cls(order_item_model.pk, order_item_model)

class OrderReceiver(object):
    def __init__(self, pk, order_receiver_model_obj=None):
        self.pk = pk
        self.__model_obj = order_receiver_model_obj

    @classmethod
    def get_order_receiver(cls, order_sn):
        recevier_model = OrderReceiverModel.objects.get(
                order_sn=order_sn)
        return cls(recevier_model.pk, recevier_model)

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
