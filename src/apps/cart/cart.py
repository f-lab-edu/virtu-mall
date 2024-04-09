from abc import ABC
from abc import abstractmethod
from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart
from apps.product.models import Product


class BaseCart(ABC):
    @abstractmethod
    def add(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def remove(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def get_items(self):
        pass


class SessionCart(BaseCart):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, request, *args, **kwargs):
        """
        Add a product to the cart or update its quantity.
        """
        product = get_object_or_404(Product, id=request.data.get("product"))
        quantity = request.data.get("quantity", 1)
        override_quantity = request.data.get("override", False)

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += int(quantity)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, request, *args, **kwargs):
        """
        Remove a product from the cart.
        """
        product = get_object_or_404(Product, id=request.data.get("product"))
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_items(self):
        return list(self.__iter__())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )


class DBCart(BaseCart):
    def __init__(self, user, instance):
        self.user = user
        self.instance = instance

    def add(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=request.data.get("product"))
        quantity = request.data.get("quantity", 1)
        override_quantity = request.data.get("override", False)

        cart_item, created = Cart.objects.get_or_create(
            user=self.user, product=product, defaults={"quantity": quantity}
        )
        if created:
            cart_item.save()
            return

        if not override_quantity:
            request.data["quantity"] += cart_item.quantity
        self.instance.update(request, *args, **kwargs)

    def remove(self, request, *args, **kwargs):
        self.instance.destroy(request, *args, **kwargs)

    def get_items(self):
        return Cart.objects.filter(user=self.user)
