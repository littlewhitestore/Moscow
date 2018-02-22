# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class StatusBase(object):

    @classmethod
    def dict(cls):
        raise Exception("Status class [%s] doesn't implement method dict()!"%cls.__name__) 

    @classmethod
    def _list(cls):
        _dict = cls.dict()
        return _dict.keys()
    
    @classmethod
    def all(cls):
        _dict = cls.dict()
        _all = []
        for key in cls._list():
            _all.append({
                'key': key,
                'value': _dict[key]
            })
        return _all

    @classmethod
    def value_to_text(cls, value):
        _dict = cls.dict()
        if _dict.has_key(value):
            return _dict[value]
        return None
