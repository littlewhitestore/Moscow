# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common.services.user import User

def check_token(func):
    def wrapper(self, request, *args, **kwargs):
        token = None
        if hasattr(request, 'GET'):
            token = request.GET.get('token', None)
        elif hasattr(request, 'POST'):
            token = request.GET.get('token', None)
        else:
            raise Exception('object type %s has no GET nor POST attribute.'%type(request))
        request.user_obj = User.fetch_user_by_token(token)  
        return func(self, request, *args, **kwargs)
    return wrapper
