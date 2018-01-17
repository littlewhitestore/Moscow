# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
import time

class ApiJsonResponse(JsonResponse):
    
    def __init__(self, data={}, success=True, message=''):
        timestamp = int(time.time())
        if success == True:
            status = 'success'
        else:
            status = 'error'
        res = {
            'status': status, 
            'message': message,
            'data': data,
            'timestamp': timestamp
        }
        super(ApiJsonResponse, self).__init__(res)
        
