from django.urls import path

from . import views

urlpatterns = [
    path("signup/buyer/", views.BuyerSignUpView.as_view(), name="buyer-signup"),
    path("signup/store/", views.StoreSignUpView.as_view(), name="store-signup"),
    path("buyer/<int:pk>/", views.BuyProfileDetail.as_view(), name="buyer-detail"),
    path("store/<int:pk>/", views.StoreProfileDetail.as_view(), name="store-detail"),
    path("login/", views.login_view, name="user-login"),
    path("logout/", views.logout_view, name="user-logout"),
]
