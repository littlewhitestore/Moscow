# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json
import hashlib

from .models import GoodsModel, GoodsBannerImageModel, GoodsDetailImageModel, GoodsSkuModel

class GoodsStatus(object):
    FREEZED = 0
    NORMAL = 1

    @classmethod
    def dict(cls):
        return {
            cls.FREEZED: "冻结",
            cls.NORMAL: "正常",
        }

class SkuStatus(object):
    FREEZED = 0
    NORMAL = 1

    @classmethod
    def dict(cls):
        return {
            cls.FREEZED: "下架",
            cls.NORMAL: "上架",
        }


class Goods(object):

    def __init__(self, id, goods_model_obj=None):
        self.__id = int(id)
        self.__goods_model_obj = goods_model_obj
        self.__goods_banner_image_list = None
        self.__goods_detail_image_list = None
        self.__goods_sku_model_dict = None

    def __confirm_goods_obj(self):
        if self.__goods_model_obj == None:
            self.__goods_model_obj = GoodsModel.objects.get(pk=self.__id)

    def __confirm_goods_banner_image_model(self):
        if self.__goods_banner_image_list == None:
            self.__goods_banner_image_list = []
            for obj in GoodsBannerImageModel.objects.filter(goods_id=self.id).order_by('sort'):
                self.__goods_banner_image_list.append(obj.url)

    def __confirm_goods_detail_image_model(self):
        if self.__goods_detail_image_list == None:
            self.__goods_detail_image_list = []
            for obj in GoodsBannerImageModel.objects.filter(goods_id=self.id).order_by('sort'):
                self.__goods_detail_image_list.append(obj.url)
    
    def __confirm_goods_sku_model_dict(self):
        if self.__goods_sku_model_dict == None:
            self.__goods_sku_model_dict = {}
            for obj in GoodsSkuModel.objects.filter(goods_id=self.id, status=SkuStatus.NORMAL).order_by('created_time'):
                self.__goods_sku_model_dict[obj.id] = obj

    def __is_property_vector_conflict(self, pv_a, pv_b):
        if len(pv_a) != len(pv_b):
            return True
        i = 0
        flag_same_value = True 
        while i < len(pv_a):
            if pv_a[i]['key'] != pv_b[i]['key']:
                return True
            if pv_a[i]['value'] != pv_b[i]['value']:
                flag_same_value = False 
            i += 1
        if flag_same_value == True:
            return True
        return False
    
    @property
    def id(self):
        return self.__id

    @classmethod
    def create(cls, name, price, market_price, taobao_id='', status=GoodsStatus.NORMAL,
        banner_image_list=None, detail_image_list=None):

        goods_model_obj = GoodsModel(
            name=name,
            price=price,
            market_price=market_price,
            taobao_id=taobao_id,
            status=status
        )
        goods_model_obj.save()

        obj = cls(goods_model_obj.id, goods_model_obj)
        if banner_image_list != None and len(banner_image_list) > 0:
            obj.update_banner_image_list(banner_image_list)

        if detail_image_list != None and len(detail_image_list) > 0:
            obj.update_detail_image_list(detail_image_list)

        return obj
   
    @classmethod
    def _filter(cls, fargs={}, qexp=None):
        hdl = GoodsModel.objects.all()
        if fargs != None and len(fargs) > 0:
            hdl = hdl.filter(**fargs)
        if qexp != None:
            hdl = hdl.filter(qexp)
        return hdl 
        
    @classmethod
    def fetch(cls, fargs={}, qexp=None, offset=0, count=20):
        hdl = cls._filter(fargs, qexp)
        hdl = hdl[offset : offset + count]
        obj_list = map(lambda _m: cls(_m.pk, _m), hdl)
        return obj_list

    
    @classmethod
    def fetch_recommend_goods(cls, offset=0, count=20):
        goods_obj_list = []
        for goods_model_obj in GoodsModel.objects.filter(status=GoodsStatus.NORMAL).order_by('-created_time')[offset : offset + count]:
            goods_obj_list.append(cls(goods_model_obj.id, goods_model_obj))
        return goods_obj_list


    @classmethod
    def fetch_by_sku(cls, sku_id):
        sku_id = int(sku_id)
        goods_sku_obj = GoodsSkuModel.objects.get(pk=sku_id)
        goods_id = goods_sku_obj.goods_id
        return cls(goods_id)
            

    def add_sku(self, image_url, property_vector, price, stock=0, status=SkuStatus.NORMAL):
        self.__confirm_goods_sku_model_dict()
        for obj in self.__goods_sku_model_dict.values():
            if self.__is_property_vector_conflict(property_vector, json.loads(obj.property_vector)):
                raise Exception("property_vector conflict!")
        
        obj = GoodsSkuModel(
            goods_id=self.id,
            image_url=image_url,
            property_vector=json.dumps(property_vector),
            price=price,
            stock=stock,
            status=status
        )
        obj.save()
        self.__goods_sku_model_dict[obj.id] = obj
        return obj.id


    def read(self):
        self.__confirm_goods_obj()
        self.__confirm_goods_banner_image_model()
        self.__confirm_goods_detail_image_model()
        goods_info = {
            'id': self.__goods_model_obj.id,
            'name': self.__goods_model_obj.name,
            'price': self.__goods_model_obj.price,
            'market_price': self.__goods_model_obj.market_price,
            'status': self.__goods_model_obj.status,
            'status_text': GoodsStatus.dict()[self.__goods_model_obj.status],
            'banner_image_list': self.__goods_banner_image_list,
            'detail_image_list': self.__goods_detail_image_list,
        }
        return goods_info
    
    def __serialize_sku_property_vector(self, property_vector):
        property_vector = json.loads(property_vector)
        property_str_list = []
        for property_item in property_vector:
            property_str_list.append(property_item['key'] + ':' + property_item['value'])
        return ';'.join(property_str_list)
    
    def get_sku_info(self, sku_id):
        sku_id = int(sku_id)
        self.__confirm_goods_obj()
        self.__confirm_goods_sku_model_dict()
        if not self.__goods_sku_model_dict.has_key(sku_id):
            raise Exception("sku %d is not related to goods %d"%(sku_id, self.id))
        
        sku_obj = self.__goods_sku_model_dict[sku_id]
        sku_info = {
            'id': sku_obj.id,
            'goods_id': self.id, 
            'goods_name': self.__goods_model_obj.name,
            'price': sku_obj.price, 
            'image_url': sku_obj.image_url, 
            'property': self.__serialize_sku_property_vector(sku_obj.property_vector), 
        }
        return sku_info
        

    def fetch_sku_all(self):
        self.__confirm_goods_sku_model_dict()
        sku_list = []
        for sku in sorted(self.__goods_sku_model_dict.values(), key=lambda x: x.created_time):
            sku_list.append({
                'id': sku.id,
                'image_url': sku.image_url,
                'property_vector': json.loads(sku.property_vector),
                'price': sku.price,
                'stock': sku.stock,
            })
        return sku_list


    def update(self, **update):
        self.__confirm_goods_obj()

        is_changed = False
        if 'name' in kwargs:
            self.__goods_model_obj.name = kwargs['name']
            is_changed = True
        if 'price' in kwargs:
            self.__goods_model_obj.price = int(kwargs['price'])
            is_changed = True
        if 'market_price' in kwargs:
            self.__goods_model_obj.market_price = int(kwargs['market_price'])
            is_changed = True
        if 'status' in kwargs:
            self.__goods_model_obj.status = int(kwargs['status'])
            is_changed = True

        if is_changed == True:
            self.__goods_model_obj.save()


    def update_banner_image_list(self, banner_image_list):
        GoodsBannerImageModel.objects.filter(goods_id=self.id).delete()
        sort = 1
        for image_url in banner_image_list:
            image_obj = GoodsBannerImageModel(
                goods_id=self.id,
                url=image_url,
                sort=sort
            )
            image_obj.save()
            sort += 1


    def update_detail_image_list(self, detail_image_list):
        GoodsDetailImageModel.objects.filter(goods_id=self.id).delete()
        sort = 1
        for image_url in detail_image_list:
            image_obj = GoodsDetailImageModel(
                goods_id=self.id,
                url=image_url,
                sort=sort
            )
            image_obj.save()
            sort += 1
