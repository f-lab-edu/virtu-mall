from datetime import datetime
from typing import Any
from typing import Dict

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.payment.models import Order
from apps.payment.models import OrderDetail
from apps.payment.models import Wallet
from apps.user.models import User


def update_wallet_transaction(user: User, total_price: int) -> None:
    wallet = Wallet.objects.select_for_update().get(user=user)
    if wallet.balance < total_price:
        raise ValidationError("update_wallet_transaction failed")
    wallet.last_transaction_ts = datetime.now()
    wallet.last_transaction_amount = total_price
    wallet.balance -= total_price
    wallet.save()


def update_product_stock(order_detail_data: Dict[str, Any]) -> None:
    for detail_data in order_detail_data:
        product = detail_data["product"]
        if detail_data["quantity"] > product.stock:
            raise ValidationError("update_product_stock failed")
        product.stock -= detail_data["quantity"]
        product.save()


@transaction.atomic
def pay(user: User, total_price: int, order_detail_data: Dict[str, Any]):
    update_wallet_transaction(user, total_price)
    update_product_stock(order_detail_data)


@transaction.atomic
def rollback_pay(user: User, order: Order):
    wallet = Wallet.objects.select_for_update().get(user=user)
    wallet.balance += order.total_price
    wallet.save()

    order_detail = OrderDetail.objects.filter(order=order)

    for detail_data in order_detail:
        product = detail_data.product
        product.stock += detail_data.quantity
        product.save()

    order.status = 5
    order.save()
    return order
