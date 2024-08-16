from datetime import datetime
from typing import Any
from typing import Dict

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.exceptions import ValidationError

from apps.payment.models.order import Order
from apps.payment.models.order import OrderDetail
from apps.payment.models.wallet import Wallet


def check_product_stock(order_detail_data: dict[str, Any]) -> None:
    for detail_data in order_detail_data:
        product = detail_data["product"]
        if product.deleted_at is not None:
            raise ValidationError("update_product_stock failed: invalid product")

        stock = (
            product.stock
            - OrderDetail.objects.filter(product=product, deleted_at=None).aggregate(
                stock=Coalesce(Sum("quantity"), 0)
            )["stock"]
        )
        if detail_data["quantity"] > stock:
            raise ValidationError("update_product_stock failed")


def update_wallet_transaction(
    order: dict[str, Any], order_detail_data: dict[str, Any]
) -> None:
    balance = Wallet.get_balance(user=order["user"])
    if balance < order["total_price"]:
        raise ValidationError("update_wallet_transaction failed")

    create_order_details(order, order_detail_data)
    return Wallet.objects.create(
        user=order["user"],
        transaction_type=Wallet.TransactionType.WITHDRAWAL,
        amount=order["total_price"],
        mileage=order["total_price"] * 0.03,
    )


def create_order_details(self, order: Order, order_detail_data: dict[str, Any]) -> None:
    OrderDetail.objects.bulk_create(
        [OrderDetail(order=order, **detail_data) for detail_data in order_detail_data]
    )


@transaction.atomic
def pay(order: Dict[str, Any], order_detail_data: dict[str, Any]) -> None:
    check_product_stock(order_detail_data)
    return update_wallet_transaction(order, order_detail_data)


@transaction.atomic
def rollback_pay(order: Order) -> None:
    now = datetime.utcnow()
    order.status = Order.Status.CANCELED
    order.deleted_at = now
    order.save()

    Wallet.objects.filter(order=order).update(deleted_at=now)
    OrderDetail.objects.filter(order=order).update(deleted_at=now)
