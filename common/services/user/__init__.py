# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
import datetime
import hashlib

from .models import UserModel
from .WXBizDataCrypt import WXBizDataCrypt

class User(object):

    def __init__(self, id, user_model_obj=None):
        self.__id = int(id)
        self.__user_model_obj = user_model_obj

    def __confirm_user_obj(self):
        if self.__user_model_obj == None:
            self.__user_model_obj = UserModel.objects.get(pk=self.__id)

    @property
    def id(self):
        return self.__id

    @property
    def entry(self):
        self.__confirm_user_obj()
        return self.__user_model_obj.entry
    
    @property
    def token(self):
        self.__confirm_user_obj()
        return self.__user_model_obj.token

    @property
    def openid(self):
        self.__confirm_user_obj()
        return self.__user_model_obj.wx_openid

    @classmethod
    def fetch_user_by_wx_openid(cls, entry, openid):
        try:
            user_model_obj = UserModel.objects.get(
                entry=entry,
                wx_openid=openid
            )
            obj = cls(user_model_obj.id, user_model_obj)
            return obj
        except Exception:
            pass
        return None

    @classmethod
    def fetch_user_by_token(cls, entry, token):
        try:
            user_model_obj = UserModel.objects.get(
                token=token
            )
            obj = cls(user_model_obj.id, user_model_obj)
            return obj
        except Exception:
            pass
        return None

    @classmethod
    def create(cls, entry, wx_openid, wx_session_key):
        user_model_obj = UserModel(
            entry=entry,
            wx_openid=wx_openid,
            wx_session_key=wx_session_key
        )
        user_model_obj.save()
        return cls(user_model_obj.id, user_model_obj)


    def update_token(self, additional_info, wx_session_key):
        self.__confirm_user_obj()

        info_str = str(self.id) + str(datetime.datetime.now()) + self.__user_model_obj.wx_openid
        info_str = self.__user_model_obj.entry + info_str
        if additional_info != None:
            info_str += additional_info
        hash_md5_obj = hashlib.md5(info_str)

        self.__user_model_obj.token = hash_md5_obj.hexdigest()
        self.__user_model_obj.wx_session_key = wx_session_key 
        self.__user_model_obj.save()

    
    def get_wx_encrypted_data(self, encryptedData, iv):
        self.__confirm_user_obj()
        
        wechat_app_id = settings.ENTRY_CONFIG[self.entry]['WECHAT_APP_ID']
        pc = WXBizDataCrypt(wechat_app_id, self.__user_model_obj.wx_session_key)
        data = pc.decrypt(encryptedData, iv)
        
        if data.has_key('unionId'):
            self.__user_model_obj.wx_unionid = data['unionId']
            self.__user_model_obj.save()
        
