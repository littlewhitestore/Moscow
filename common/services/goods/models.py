# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class GoodsModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    taobao_id = models.CharField(max_length=128, default='', db_index=True)
    market_price = models.IntegerField(null=False, db_index=True)
    price = models.IntegerField(null=False, db_index=True)
    status = models.IntegerField(null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'goods'

class GoodsSkuModel(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField(null=False, db_index=True)
    image_url = models.CharField(max_length=1024, default='')
    property_vector = models.CharField(max_length=512, default='')
    market_price = models.IntegerField(null=False, db_index=True)
    price = models.IntegerField(null=False, db_index=True)
    stock = models.IntegerField(null=False, db_index=True)
    status = models.IntegerField(null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'goods_sku'

class GoodsBannerImageModel(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField(null=False, db_index=True)
    url = models.CharField(max_length=1024, default='')
    sort = models.IntegerField(null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'goods_banner_image'


class GoodsDetailImageModel(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField(null=False, db_index=True)
    url = models.CharField(max_length=1024, default='')
    sort = models.IntegerField(null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_detail_image'
