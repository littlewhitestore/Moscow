# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import hashlib

class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    market_price = models.IntegerField(null=False, db_index=True)
    price = models.IntegerField(null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

