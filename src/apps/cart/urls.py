from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.CartViewSet.as_view({"get": "list"}),
    ),
    path(
        "add/",
        views.CartViewSet.as_view({"post": "add"}),
    ),
    path(
        "remove/",
        views.CartViewSet.as_view({"post": "remove"}),
    ),
]
