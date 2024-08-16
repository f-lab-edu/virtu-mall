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


class StockChecker:
    def check_stock(self, order_detail_data: dict[str, Any]) -> None:
        for detail_data in order_detail_data:
            product = detail_data["product"]
            if product.deleted_at is not None:
                raise ValidationError("update_product_stock failed: invalid product")

            stock = (
                product.stock
                - OrderDetail.objects.filter(
                    product=product, deleted_at=None
                ).aggregate(stock=Coalesce(Sum("quantity"), 0))["stock"]
            )
            if detail_data["quantity"] > stock:
                raise ValidationError("update_product_stock failed")


class WalletManager:
    def update_transaction(self, order: dict[str, Any]) -> None:
        balance = Wallet.get_balance(user=order["user"])
        if balance < order["total_price"]:
            raise ValidationError("update_wallet_transaction failed")

        return Wallet.objects.create(
            user=order["user"],
            transaction_type=Wallet.TransactionType.WITHDRAWAL,
            amount=order["total_price"],
            mileage=order["total_price"] * 0.03,
        )

    def delete_transaction(self, order: Order) -> None:
        Wallet.objects.filter(order=order).update(deleted_at=order.deleted_at)


class OrderDetailManager:
    def __init__(self, stock_checker: StockChecker):
        self.stock_checker = stock_checker

    def create(self, order: dict[str, Any], order_detail_data: dict[str, Any]) -> None:
        self.stock_checker.check_stock(order_detail_data)
        OrderDetail.objects.bulk_create(
            [
                OrderDetail(order=order, **detail_data)
                for detail_data in order_detail_data
            ]
        )

    def delete(self, order: Order) -> None:
        OrderDetail.objects.filter(order=order).update(deleted_at=order.deleted_at)


class PayService:
    def __init__(
        self,
        order_detail_manager: OrderDetailManager,
        wallet_manager: WalletManager,
    ):
        self.order_detail_manager = order_detail_manager
        self.wallet_manager = wallet_manager

    @transaction.atomic
    def pay(self, order: Dict[str, Any], order_detail_data: dict[str, Any]) -> None:
        self.order_detail_manager.create(order, order_detail_data)
        self.wallet_manager.update_transaction(order)

    @transaction.atomic
    def rollback_pay(self, order: Order) -> None:
        now = datetime.utcnow()
        order.status = Order.Status.CANCELED
        order.deleted_at = now
        order.save()

        self.wallet_manager.delete_transaction(order)
        self.order_detail_manager.delete(order)


stock_checker = StockChecker()
order_detail_manager = OrderDetailManager(stock_checker)
wallet_manager = WalletManager()
pay_service = PayService(wallet_manager, order_detail_manager)
