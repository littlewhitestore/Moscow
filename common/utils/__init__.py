# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import hashlib
import pytz
import time

def _append_tz(t):
    tz = pytz.timezone(settings.TIME_ZONE)
    return tz.localize(t)

def generate_image_url(image_key):
    return "https://www.xiaobaidian.cn/static/img/%s.jpg"%image_key

def epoch(t):
    """Date/Time converted to seconds since epoch"""
    if not hasattr(t, 'tzinfo'):
        return
    return int(time.mktime(_append_tz(t).timetuple()))


class ImageStorage(object):
    BUCKET_SIZE = 16
    QCLOUD_CONFIG = {
        'secret_id': 'AKIDjOTO9qnlxyoBe2aJB2vmTzKVYVL5m6NT',
        'secret_key': '65t0xlYEnCQn2771nR3Ys18A2oT3Yy31',
        'region': 'ap-beijing',
    }
    
    @staticmethod
    def generate_stream_key(stream):
        handler = hashlib.md5().update(stream)
        key = handler.hexdigest()
        return key
    
    @staticmethod
    def get_bucket_by_key(key):
        bucket = "img-prod-{:0>3d}-1255633922".format(hash(key) % ImageStorage.BUCKET_SIZE + 1)
        #change to the first char of md5 hash
        return bucket

    @staticmethod
    def get_url_by_key(key):
        pass
        
