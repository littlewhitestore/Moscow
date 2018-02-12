# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from common.services.user import User
from .response import ApiJsonResponse, ApiResponseStatusCode

def check_token(func):
    def wrapper(self, request, *args, **kwargs):
        entry = None
        token = None
        if request.method == 'GET': 
            token = request.GET.get('token', None)
            entry = request.GET.get('entry', None)
        elif request.method == 'POST':
            token = request.data.get('token', None)
            entry = request.data.get('entry', None)
        else:
            raise Exception('object type %s has no GET nor POST attribute.'%type(request))
        
        if entry == None:
            raise Exception('failed to get entry.')
        entry = entry.lower()
        
        if not settings.ENTRY_CONFIG.has_key(entry):
            raise Exception('wrong entry [%s].'%entry)

        
        request.user_obj = User.fetch_user_by_token(entry, token)
        request.entry = entry
        return func(self, request, *args, **kwargs)
    return wrapper

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user_obj == None:
            return ApiJsonResponse({}, status_code=ApiResponseStatusCode.RELOGIN)  
        return func(self, request, *args, **kwargs)
    return wrapper
