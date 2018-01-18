# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common.models import User

def check_session(func):
    def wrapper(self, request, *args, **kwargs):
        session = None
        if hasattr(request, 'GET'):
            session = request.GET.get('session', None)
        elif hasattr(request, 'POST'):
            session = request.GET.get('session', None)
        else:
            raise Exception('object type %s has no GET nor POST attribute.'%type(request))
        request.user_obj = User.fetch_user_by_session(session)  
        return func(self, request, *args, **kwargs)
    return wrapper
