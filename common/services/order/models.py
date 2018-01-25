# *-* coding:utf-8 *-*

from __future__ import unicode_literals

from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_sn = models.CharField(max_length=32, unique=True)
    user_id = models.IntegerField()
    total_amount = models.IntegerField(default=0)
    postage = models.IntegerField(default=0)
    amount_payable = models.IntegerField(default=0)
    order_status = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oms_order'

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
                address=address)

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order_sn = models.CharField(max_length=32)
    goods_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=64, blank=True)
    market_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oms_order_item'


class OrderReceiver(models.Model):
    id = models.AutoField(primary_key=True)
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
        db_table = 'oms_order_receiver'
