# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import views

from common.services.settlement import SettlementManager 
from .decorators import check_token, login_required
from .response import ApiJsonResponse

class SettlementBuyNowView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        sku_id = int(request.data.get('sku_id'))
        number = int(request.data.get('number', '1'))
        receiver = request.data.get('receiver', None)

        user_id = request.user_obj.id
        user_openid = request.user_obj.openid
        mgr = SettlementManager(user_id, user_openid)
        settlement_info = mgr.buynow_settlement(sku_id, number)
        
        data = {
            'items': settlement_info['item_list'],
            'total_amount': str(float(settlement_info['total_amount'] / 100.0)),
            'amount_payable': str(float(settlement_info['amount_payable'] / 100.0))
        }
        if receiver is not None:
            data['receiver'] = receiver
        
        return ApiJsonResponse(data)

class OrderCreateBuyNowView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        sku_id = int(request.data.get('sku_id'))
        number = int(request.data.get('number', '1'))
        receiver = request.data.get('receiver')
        
        
        entry = request.entry
        user_id = request.user_obj.id
        user_openid = request.user_obj.openid

        mgr = SettlementManager(user_id, user_openid)
        checkout_info = mgr.buynow_checkout(
            entry=entry,
            sku_id=sku_id,
            number=number,
            receiver=receiver
        )

        return ApiJsonResponse(checkout_info)

class SettlementPintuanView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        sku_id = int(request.data.get('sku_id'))
        number = int(request.data.get('number'))
        receiver = request.data.get('receiver', None)
        pintuan_sn = request.data.get('pintuan_sn', None)
        
        pintuan_sn = '19871656608817762094'

        user_id = request.user_obj.id
        user_openid = request.user_obj.openid
        mgr = SettlementManager(user_id, user_openid)

        if pintuan_sn == None:
            settlement_info = mgr.pintuan_create_settlement(sku_id, number)
        else:
            settlement_info = mgr.pintuan_join_settlement(pintuan_sn, number)
            
        data = {
            'items': settlement_info['item_list'],
            'total_amount': str(float(settlement_info['total_amount'] / 100.0)),
            'amount_payable': str(float(settlement_info['amount_payable'] / 100.0))
        }
        if receiver is not None:
            data['receiver'] = receiver
        
        return ApiJsonResponse(data)

class OrderCreatePintuanView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        sku_id = int(request.data.get('sku_id'))
        number = int(request.data.get('number'))
        receiver = request.data.get('receiver')
        pintuan_sn = request.data.get('pintuan_sn', None)
        
        pintuan_sn = '19871656608817762094'
        
        entry = request.entry
        user_id = request.user_obj.id
        user_openid = request.user_obj.openid

        mgr = SettlementManager(user_id, user_openid)
        if pintuan_sn == None:
            checkout_info = mgr.pintuan_create_checkout(
                entry=entry,
                sku_id=sku_id,
                number=number,
                receiver=receiver
            )
        else:
            checkout_info = mgr.pintuan_join_checkout(
                entry=entry,
                pintuan_sn=pintuan_sn,
                number=number,
                receiver=receiver
            )
            
        return ApiJsonResponse(checkout_info)
