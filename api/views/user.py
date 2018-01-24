# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from common.services.user import User
from rest_framework import views
from .response import ApiJsonResponse
import requests

class Login(views.APIView):
    
    def get(self, request):
        code = request.GET.get("code", None)
        if code != None:
            url = 'https://api.weixin.qq.com/sns/jscode2session'
            payload = {
                'appid': settings.WECHAT_APP_ID,
                'secret': settings.WECHAT_APP_SECRET,
                'js_code': code,
                'grant_type': 'authorization_code'
            }
            ret = requests.get(url, params=payload)
            ret_data = ret.json()
            wx_openid = ret_data['openid']
            wx_session_key = ret_data['session_key']

            user_obj = User.fetch_user_by_wx_openid(wx_openid)
            if user_obj == None:
                user_obj = User.create(wx_openid, wx_session_key)
            user_obj.update_session(additional_info=code)

        res = {
            'session': user_obj.session 
        }
        return ApiJsonResponse(res)

