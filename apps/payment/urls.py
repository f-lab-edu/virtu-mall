from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"wallet", views.WalletViewSet, basename="wallet")
router.register(r"order", views.OrderViewSet, basename="order")
router.register(r"order-detail", views.OrderDetailViewSet, basename="order-detail")

urlpatterns = [
    path("", include(router.urls)),
]
