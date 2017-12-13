# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
