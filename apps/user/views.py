from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers import UserSerializer
from utils.permissions import IsOwner


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsOwner]


@api_view(["POST"])
def sign_up_view(request):
    user = {
        "username": request.data.get("username"),
        "password": request.data.get("password"),
        "name": request.data.get("name"),
        "address": request.data.get("address"),
        "phone": request.data.get("phone"),
        "email": request.data.get("email"),
    }
    User.objects.create_user(**user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
