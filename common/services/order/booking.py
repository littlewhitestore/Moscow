# *-* coding:utf-8 *-*

from .models import Order, OrderItem
from .snowflake import sn

class OrderBookingService(object):
    def booking(self, user, check_list):
        order = Order.objects.create(
                order_sn='18' + str(sn()),
                user_id=user.id, # 需要使用正常的用户ID
                total_amount=check_list.total_amount,
                amount_payable=check_list.amount_payable,
                postage=check_list.postage)

        for item in check_list.product_list:
            OrderItem.objects.create(
                    order=order,
                    goods_id=item.product.goods_id,
                    product_id=item.product.product_id,
                    product_name=item.product.name,
                    market_price=item.product.market_price,
                    sale_price=item.product.price,
                    number=item.number)

        receiver = check_list.receiver

        order.set_receiver(
                name=receiver.get('name'),
                mobile=receiver.get('mobile'),
                province=receiver.get('province'),
                city=receiver.get('city'),
                district=receiver.get('district'),
                address=receiver.get('address'))
