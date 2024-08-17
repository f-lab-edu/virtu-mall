from datetime import datetime
from typing import Any
from typing import Dict

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.payment.models.order import Order
from apps.payment.models.wallet import Wallet
from apps.product.models import Product


class ProductManager:
    def check_and_update_stock(self, order_detail_data: Dict[str, Any]) -> None:
        for detail_data in order_detail_data:
            product = Product.objects.select_for_update().get(
                id=detail_data.get("product")
            )

            self._validate_product(product, detail_data["quantity"])
            self._update_stock(product, detail_data["quantity"])

    def _validate_product(self, product: Product, quantity: int) -> None:
        if product.deleted_at is not None:
            raise ValidationError("update_product_stock failed: invalid product")

        if quantity > product.stock:
            raise ValidationError("update_product_stock failed: insufficient stock")

    def _update_stock(self, product: Product, quantity: int) -> None:
        product.stock -= quantity
        product.save()


class WalletManager:
    def update_transaction(self, order: dict[str, Any]) -> None:
        wallet = Wallet.objects.select_for_update().get(user=order["user"])
        total_price = order["total_price"]

        if wallet.balance < total_price:
            raise ValidationError("update_wallet_transaction failed")
        wallet.balance -= total_price
        wallet.mileage += total_price * 0.03
        wallet.save()

    def delete_transaction(self, order: Order) -> None:
        wallet = Wallet.objects.select_for_update().get(user=order["user"])
        total_price = order["total_price"]
        wallet.balance += total_price
        wallet.mileage -= total_price * 0.03
        wallet.save()


class PayService:
    def __init__(
        self,
        product_manager: ProductManager,
        wallet_manager: WalletManager,
    ):
        self.product_manager = product_manager
        self.wallet_manager = wallet_manager

    @transaction.atomic
    def pay(self, order: Dict[str, Any], order_detail_data: dict[str, Any]) -> None:
        self.product_manager.check_and_update_stock(order_detail_data)
        self.wallet_manager.update_transaction(order)

    @transaction.atomic
    def rollback_pay(self, order: Order) -> None:
        now = datetime.utcnow()
        order.status = Order.Status.CANCELED
        order.deleted_at = now
        order.save()

        self.wallet_manager.delete_transaction(order)
        # self.order_detail_manager.delete(order)


product_manager = ProductManager()
wallet_manager = WalletManager()
pay_service = PayService(product_manager, wallet_manager)
