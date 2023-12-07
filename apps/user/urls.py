from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserList.as_view(), name="user-list"),
    path("<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("signup", views.sign_up_view, name="user-signup"),
    path("login", views.login_view, name="user-login"),
    path("logout", views.logout_view, name="user-logout"),
]
