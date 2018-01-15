# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import hashlib

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    session = models.CharField(max_length=256, default='', db_index=True)
    wx_openid = models.CharField(max_length=256, db_index=True)
    wx_unionid = models.CharField(max_length=256, default='', db_index=True)
    wx_session_key = models.CharField(max_length=256, default='', db_index=True)
    
    def update_session(self, additional_info=''):
        info_str = str(self.id) + str(datetime.datetime.now()) + self.wx_openid
        if additional_info != None:
            info_str += additional_info
        
        hash_md5_obj = hashlib.md5(info_str)
        self.session = hash_md5_obj.hexdigest()
        self.save()

    @classmethod
    def fetch_user_by_wx_openid(cls, openid):
        try:
            obj = cls.objects.get(wx_openid=openid)
            return obj
        except Exception:
            pass
        return None

