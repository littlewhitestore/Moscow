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
    updated_time = models.DateTimeField(auto_now_add=True)

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

    @classmethod
    def fetch_user_by_session(cls, session):
        try:
            obj = cls.objects.get(session=session)
            return obj
        except Exception:
            pass
        return None

