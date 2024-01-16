from typing import Any

import pytest
from rest_framework.exceptions import ValidationError

from apps.payment.models.wallet import Wallet
from apps.payment.services import check_product_stock
from apps.payment.services import update_wallet_transaction


@pytest.mark.parametrize(
    "quantity, should_raise",
    [
        (4, False),  # stock:5, order quantity:4
        (6, True),  # stock:5, order quantity:6 -> raiseError
    ],
)
def test_check_stock(
    mocker: pytest.MockFixture, quantity: int, should_raise: bool
) -> None:
    mocker.patch(
        "apps.payment.models.order.OrderDetail.objects.filter",
        return_value=mocker.Mock(aggregate=lambda **kwargs: {"stock": 5}),
    )

    product_mock = mocker.Mock(stock=10, deleted_at=None)
    order_detail_data = [{"product": product_mock, "quantity": quantity}]

    if should_raise:
        with pytest.raises(ValidationError):
            check_product_stock(order_detail_data)
    else:
        try:
            check_product_stock(order_detail_data)
        except ValidationError:
            pytest.fail("Unexpected ValidationError raised")


@pytest.mark.parametrize(
    "order, balance, expected_exception",
    [
        ({"user": "user123", "total_price": 1000}, 1000, None),  # 충분한 잔액
        ({"user": "user123", "total_price": 2000}, 1000, ValidationError),  # 부족한 잔액
    ],
)
def test_update_wallet_transaction(
    mocker: pytest.MockFixture,
    order: dict[str, str | bool],
    balance: int,
    expected_exception: Any,
) -> None:
    mock_create = mocker.patch("apps.payment.models.wallet.Wallet.objects.create")

    if expected_exception:
        with pytest.raises(expected_exception):
            update_wallet_transaction(order)
    else:
        update_wallet_transaction(order)
        mock_create.assert_called_once_with(
            user=order["user"],
            transaction_type=Wallet.TransactionType.WITHDRAWAL,
            amount=order["total_price"],
            mileage=order["total_price"] * 0.03,
        )
