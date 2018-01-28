# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import hashlib

from .models import UserModel

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
    def token(self):
        self.__confirm_user_obj()
        return self.__user_model_obj.token

    @property
    def openid(self):
        self.__confirm_user_obj()
        return self.__user_model_obj.wx_openid

    @classmethod
    def fetch_user_by_wx_openid(cls, openid):
        try:
            user_model_obj = UserModel.objects.get(wx_openid=openid)
            obj = cls(user_model_obj.id, user_model_obj)
            return obj
        except Exception:
            pass
        return None

    @classmethod
    def fetch_user_by_token(cls, token):
        try:
            user_model_obj = UserModel.objects.get(token=token)
            obj = cls(user_model_obj.id, user_model_obj)
            return obj
        except Exception:
            pass
        return None

    @classmethod
    def create(cls, wx_openid, wx_session_key):
        user_model_obj = UserModel(
            wx_openid=wx_openid,
            wx_session_key=wx_session_key
        )
        user_model_obj.save()
        return cls(user_model_obj.id, user_model_obj)


    def update_token(self, additional_info=''):
        self.__confirm_user_obj()

        info_str = str(self.id) + str(datetime.datetime.now()) + self.__user_model_obj.wx_openid
        if additional_info != None:
            info_str += additional_info
        hash_md5_obj = hashlib.md5(info_str)

        self.__user_model_obj.token = hash_md5_obj.hexdigest()
        self.__user_model_obj.save()

