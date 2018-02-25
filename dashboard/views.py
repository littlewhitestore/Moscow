# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views import View
from rest_framework import views

from common.services.goods import Goods, GoodsStatus

class GoodsListView(View):
    
    def get(self, request):
        goods_obj_list = Goods.fetch()
        goods_data_list = []
        for obj in goods_obj_list:
            data = obj.read()
            sku_list = obj.fetch_sku_all()
            data['sku_number'] = len(sku_list)
            goods_data_list.append(data)
        
        context = {
            'goods_list': goods_data_list
        }
        response = TemplateResponse(request, 'goods/list.html', context)

        return response 

class GoodsEditView(View):
    
    def get(self, request, goods_id):
        goods_obj = Goods(goods_id)
        goods_info = goods_obj.read()
        sku_list = goods_obj.fetch_sku_all()
        
        context = {
            'goods_info': goods_info,
            'sku_list': sku_list,
            'goods_status_list': GoodsStatus.all(),
        }
        response = TemplateResponse(request, 'goods/edit.html', context)

        return response 
    
    def post(self, request, goods_id):
        pass

class GoodsUpload(views.APIView):

    def post(self, request):
        banner_images = request.data.get('banner_images')
        detail_images = request.data.get('detail_images')
        name = request.data.get('name')
        supply_source = request.data.get('supply_source')
        supply_item_id = request.data.get('supply_item_id')
        price = request.data.get('price')
        market_price = request.data.get('market_price')
        
        banner_image_list = banner_images.split(';')
        detail_image_list = detail_images.split(';')
        
        goods_obj = Goods.create(
            name=name,
            supply_source=supply_source,
            supply_item_id=supply_item_id,
            price=price,
            market_price=market_price,
            status=1,
            banner_image_list=banner_image_list,
            detail_image_list=detail_image_list
        )

        
        res = {
            'goods_id': goods_obj.id 
        }
        return JsonResponse(res)

class GoodsSkuUpload(views.APIView):

    def post(self, request, goods_id):
        
        property_vector_str = request.data.get('property_vector_str', None)
        if property_vector_str == None:
            property_vector = [{
                'key': u'属性',
                'value': u'默认',
            }]
        else:
            property_vector_list = property_vector_str.split('|')
            property_vector = []
            i = 0
            while (i < len(property_vector_list) and i < 4):
                property_vector.append({
                    'key': property_vector_list[i], 
                    'value': property_vector_list[i + 1], 
                })
                i += 2
        
        
        image_key = request.data.get('image_key', '')
        price = request.data.get('price', None)
        if price == None:
            raise Exception("Without price!!!")
        pintuan_price = request.data.get('pintuan_price', -1)
        stock = request.data.get('stock', 1000)
        supply_cost = request.data.get('supply_cost', -1)
        
        
        goods_obj = Goods(goods_id)
        sku_id = goods_obj.add_sku(
            image_key=image_key,
            property_vector=property_vector, 
            price=price,
            pintuan_price=pintuan_price,
            supply_cost=supply_cost,
            stock=stock,
        )

        
        res = {
            'goods_id': goods_obj.id, 
            'sku_id': sku_id 
        }
        return JsonResponse(res)
