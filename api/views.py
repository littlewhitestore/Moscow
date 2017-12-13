# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import views, status


class HelloWorld(views.APIView):
    
    def get(self):
        return HiResponse(code="MISS_PARAMS", message="缺少参数")
