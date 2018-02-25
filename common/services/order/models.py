# *-* coding:utf-8 *-*

from __future__ import unicode_literals

from django.db import models

class OrderModel(models.Model):
    id = models.AutoField(primary_key=True)
    entry = models.CharField(max_length=32, default='', db_index=True)
    order_sn = models.CharField(max_length=32, default='', unique=True)
    user_id = models.IntegerField(db_index=True)
    total_amount = models.IntegerField(default=0)
    postage = models.IntegerField(default=0)
    amount_payable = models.IntegerField(default=0)
    order_status = models.IntegerField(default=0, db_index=True)
    pintuan_id = models.IntegerField(default=-1, db_index=True)
    pintuan_sn = models.CharField(max_length=32, default='', db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'

    def set_receiver(self, name,
            mobile,
            province,
            city,
            district,
            address):

        OrderReceiver.objects.create(
            order=self,
            name=name,
            mobile=mobile,
            province=province,
            city=city,
            district=district,
            address=address
        )

class OrderItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(null=False, db_index=True)
    order_sn = models.CharField(max_length=32, db_index=True)
    goods_id = models.IntegerField()
    goods_name = models.CharField(max_length=64, blank=True)
    sku_id = models.IntegerField()
    sku_property = models.CharField(max_length=64, blank=True)
    sale_price = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_item'


class OrderReceiverModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(null=False, db_index=True)
    order_sn = models.CharField(max_length=32)
    name = models.CharField(max_length=32, blank=True)
    province = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=32, blank=True)
    district = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=256, blank=True)
    mobile = models.CharField(max_length=16, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_receiver'

class OrderTradeModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(null=False, db_index=True)
    order_sn = models.CharField(max_length=32, db_index=True)
    trade_no = models.CharField(max_length=32, db_index=True)
    trade_amount = models.IntegerField(default=0)
    trade_status = models.IntegerField(default=0, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_trade'

class OrderLogisticsModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(null=False, db_index=True)
    order_sn = models.CharField(max_length=32, unique=True, db_index=True)
    com = models.CharField(max_length=32)
    nu = models.CharField(max_length=32)
    data = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_logistics'

class PintuanModel(models.Model):
    id = models.AutoField(primary_key=True)
    pintuan_sn = models.CharField(max_length=32, unique=True, db_index=True)
    sku_id = models.IntegerField()
    price = models.IntegerField(null=False, db_index=True)
    success_target = models.IntegerField(default=0)
    start_user_id = models.IntegerField(db_index=True)
    pintuan_status = models.IntegerField(default=0, db_index=True)
    finish_time = models.DateTimeField(db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pintuan'

ExpressCompany = {
    'shunfeng': "顺丰快递",
    'quanritongkuaidi': "全日通",
    'yuantong': "圆通快递",
    'zhongtong': "中通快递",
    'shentong': "申通快递",
    'tiantian': "天天快递",
    'quanfengkuaidi': "全峰快递",
    'yunda': "韵达快递",
}
