# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class HomeBannerImageModel(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1024, default='')
    refer = models.CharField(max_length=1024, default='')
    sort = models.IntegerField(null=False, db_index=True)
    status = models.IntegerField(null=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'home_banner_image'


