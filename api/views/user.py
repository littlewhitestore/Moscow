# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import JsonResponse
from django.views import View

from common.models import User
import requests

class Login(View):
    
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
            openid = ret_data['openid']
            session_key = ret_data['session_key']

            user_obj = User.fetch_user_by_wx_openid(openid)
            if user_obj == None:
                user_obj = User(
                    wx_openid=openid,
                    wx_session_key=session_key
                )
                user_obj.save()
            user_obj.update_session(additional_info=code)

        res = {
            'session': user_obj.session 
        }
        return JsonResponse(res)

