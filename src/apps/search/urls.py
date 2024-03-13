from django.urls import path

from .views import SearchListAPIView

urlpatterns = [
    path("", SearchListAPIView.as_view(), name="search"),
]
