# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import hashlib
import pytz
import time

from image_storage import ImageStorage

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
