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

class BuyNowOrderView(views.APIView):

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

class SettlementPintuanCreateView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        print "testing pintuan!!!"
        sku_id = int(request.data.get('sku_id'))
        receiver = request.data.get('receiver', None)

        user_id = request.user_obj.id
        user_openid = request.user_obj.openid
        mgr = SettlementManager(user_id, user_openid)
        settlement_info = mgr.pintuan_create_settlement(sku_id)
        
        data = {
            'items': settlement_info['item_list'],
            'total_amount': str(float(settlement_info['total_amount'] / 100.0)),
            'amount_payable': str(float(settlement_info['amount_payable'] / 100.0))
        }
        if receiver is not None:
            data['receiver'] = receiver
        
        return ApiJsonResponse(data)

class OrderPintuanCreateCheckoutView(views.APIView):

    @check_token
    @login_required
    def post(self, request):
        print "test pintuan create checkout !!!"
        sku_id = int(request.data.get('sku_id'))
        receiver = request.data.get('receiver')
        
        
        entry = request.entry
        user_id = request.user_obj.id
        user_openid = request.user_obj.openid

        mgr = SettlementManager(user_id, user_openid)
        checkout_info = mgr.pintuan_create_checkout(
            entry=entry,
            sku_id=sku_id,
            receiver=receiver
        )

        return ApiJsonResponse(checkout_info)
