# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
import time


class ApiResponseStatusCode(object):
    ERROR = 0 
    SUCCESS = 1 
    RELOGIN = 2 


class ApiJsonResponse(JsonResponse):
    
    def __init__(self, data={}, status_code=ApiResponseStatusCode.SUCCESS, message=''):
        timestamp = int(time.time())
        res = {
            'status_code': status_code, 
            'message': message,
            'data': data,
            'timestamp': timestamp
        }
        super(ApiJsonResponse, self).__init__(res)
        
