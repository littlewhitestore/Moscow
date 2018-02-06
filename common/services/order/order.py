# *-* coding:utf-8 *-*
from .models import OrderModel
from .order_item import OrderItem
from .order_logistics import OrderLogistics
from .order_receiver import OrderReceiver
from .order_trade import OrderTrade
from .snowflake import sn

class OrderStatus(object):
    PENDING_PAY = 0
    PENDING_SHIP = 1
    PENDING_RECEIVE = 2
    CANCELLED = 3
    FINISH = 4

    @classmethod
    def dict(cls):
        return {
            cls.PENDING_PAY: "待支付",
            cls.PENDING_SHIP: "待发货",
            cls.PENDING_RECEIVE: "待收货",
            cls.FINISH: "已完成",
            cls.CANCELLED: "已取消",
        }

class Order(object):
    def __init__(self, order_id, model_obj=None):
        self.order_id = order_id
        self.__model_obj = model_obj
        self.__receiver = None
        self.__logistics = None
        self.__order_items = []

    @classmethod
    def get_order_list(cls, user_id, offset, count):
        qs = OrderModel.objects.filter(user_id=user_id).order_by('-created_time')
        qs = qs[offset: offset + count]
        order_list = map(lambda _m:cls(_m.pk, _m), qs)
        return order_list

    def get_status_text(self):
        self.__confirm_order_model()
        return OrderStatus.dict().get(self.__model_obj.order_status, '')

    @classmethod
    def get_order_by_sn(cls, order_sn):
        try:
            model_obj = OrderModel.objects.get(order_sn=order_sn)
            return cls(model_obj.pk, model_obj=model_obj)
        except OrderModel.DoesNotExist:
            return None

    @classmethod
    def create(cls, user_id, receiver, item_list, total_amount, amount_payable, postage=0):
        '''
        创建订单

        参数:
        @param user_id 用户ID
        @param item_list  
        @param total_amount 
        @param amount_payable 
        @param postage 
        '''
        total_amount = total_amount
        amount_payable = amount_payable
        postage = postage 
        
        order_model = OrderModel.objects.create(
            order_sn='18' + str(sn()),
            user_id=user_id,
            total_amount=total_amount,
            amount_payable=amount_payable,
            postage=postage
        )
        order_obj = cls(order_model.pk, model_obj=order_model)
        
        for item in item_list:
            sku_id = item['sku_id']
            number = item['number']
            goods_obj = Goods.fetch_by_sku(sku_id)
            sku_info = goods_obj.get_sku_info(sku_id)
            order_obj.add_order_item(
                sku_info['goods_id'],
                sku_info['id'],
                sku_info['goods_name'],
                sku_info['property'],
                sku_info['price'],
                number
            )
        
        order.set_receiver(
            receiver.get('name'),
            receiver.get('province'),
            receiver.get('city'),
            receiver.get('district'),
            receiver.get('address'),
            receiver.get('mobile'),
            receiver.get('zipcode', ''),
        )

        return order

    def pay(self, trade_no):
        order_trade = OrderTrade.from_trade_no(trade_no)
        if order_trade:
            order_trade.set_success()
            order_trade_info = order_trade.get_basic_info()
            trade_amount = order_trade_info.get('trade_amount')
            if trade_amount == self.amount_payable:
                self.set_pending_ship()

    def set_pending_ship(self):
        self.__confirm_order_model()
        self.__model_obj.order_status = OrderStatus.PENDING_SHIP
        self.__model_obj.save()

    def set_pending_receiver(self):
        self.__confirm_order_model()
        self.__model_obj.order_status = OrderStatus.PENDING_RECEIVE
        self.__model_obj.save()

    def set_cancelled(self):
        self.__confirm_order_model()
        self.__model_obj.order_status = OrderStatus.CANCELLED
        self.__model_obj.save()

    def set_pending_receive(self):
        self.__confirm_order_model()
        self.__model_obj.order_status = OrderStatus.PENDING_RECEIVE
        self.__model_obj.save()

    def set_finish(self):
        self.__confirm_order_model()
        self.__model_obj.order_status = OrderStatus.FINISH
        self.__model_obj.save()

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

    def __confirm_logistics(self):
        if self.__logistics is None:
            self.__confirm_order_model()
            self.__logistics = OrderLogistics.get_order_logistics(self.__model_obj.order_sn)

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

    @property
    def amount_payable(self):
        order_basic_info = self.get_order_basic_info()
        amount_payable = order_basic_info.get('amount_payable')
        return amount_payable

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

    def add_order_item(self, goods_id, sku_id, goods_name, sku_property, sale_price, number):
        self.__confirm_order_model()
        order_item_obj = OrderItem.create(
            self.__model_obj.order_sn,
            goods_id,
            sku_id,
            goods_name,
            sku_property,
            sale_price,
            number
        )
        return order_item_obj.id

    def apply_trade(self):
        self.__confirm_order_model()
        order_trade = OrderTrade.create(self.__model_obj.order_sn,
                self.__model_obj.amount_payable)
        return order_trade

    def get_logistics(self):
        self.__confirm_logistics()
        return self.__logistics


    def delivery(self, com, nu):
        '''
        订单发货

        参数:
        @param com: 物流公司对应的快递100的code
        @param nu:  物流单号
        '''
        self.__confirm_logistics()
        if self.__logistics is None:
            self.__logistics = OrderLogistics.create(self.__model_obj.order_sn,
                    com, nu)
            self.set_pending_receive()

    def delivery_and_subscribe(self, com, nu):
        self.delivery(com, nu)
        self.__confirm_logistics()
        self.__logistics.subscribe()

    def refresh_logistics(self, com, nu, logistics_data, is_check=False):
        '''
        更新订单的物流信息
        '''
        self.__confirm_logistics()
        logistics_basic_info = self.__logistics.get_basic_info()
        _com = logistics_basic_info.get('com')
        _nu = logistics_basic_info.get('nu')
        if com == _com and nu == _nu:
            self.__logistics.refresh(logistics_data)
            if is_check:
                self.set_finish()

