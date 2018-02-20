# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
register = template.Library()

@register.filter
def format_price(price):
    price = float(price) / 100.0
    return price
