# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.response import TemplateResponse 
from django.views import View

from common.services.goods import Goods

class GoodsListView(View):
    
    def get(self, request):
        goods_obj_list = Goods.fetch()
        goods_data_list = map(lambda _obj: _obj.read(), goods_obj_list)
        
        context = {
            'goods_list': goods_data_list
        }
        response = TemplateResponse(request, 'goods.html', context)

        return response 
