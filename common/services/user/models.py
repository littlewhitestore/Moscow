# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    entry = models.CharField(max_length=64, blank=False, db_index=True)
    token = models.CharField(max_length=256, default='', db_index=True)
    wx_openid = models.CharField(max_length=256, db_index=True)
    wx_unionid = models.CharField(max_length=256, default='', db_index=True)
    wx_session_key = models.CharField(max_length=256, default='', db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
