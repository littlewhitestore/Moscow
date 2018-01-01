# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views import View 

class Login(View):
    
    def get(self, request):
        code = request.GET.get("code", None)
        if code != None:
            pass

        res = {
            'session': '0014Rl0F1nEI410TFO1F1iWB0F14Rl0Q'
        }
        return JsonResponse(res)

