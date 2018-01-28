# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import hashlib

from .models import HomeBannerImageModel 

class HomeBanner(object):

    @staticmethod
    def add(url, refer, sort, status=1):
        obj = HomeBannerImageModel(
            url=url,
            refer=refer,
            sort=sort,
            status=status
        )
        obj.save()
    
    
    @staticmethod
    def fetch_all():
        banner_list = []
        for obj in HomeBannerImageModel.objects.filter(status=1).order_by('sort'):
            banner_list.append({
                'id': obj.id,
                'url': obj.url,
                'refer': obj.refer,
                'sort': obj.sort,
            })
        return banner_list

