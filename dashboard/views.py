# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.response import TemplateResponse 
from django.views import View

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
