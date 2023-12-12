from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.user.models import BuyerProfile, StoreProfile
from apps.user.serializers import BuyerProfileSerializer, StoreProfileSerializer
from utils.permissions import IsOwner


class BuyerSignUpView(CreateAPIView):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer


class StoreSignUpView(CreateAPIView):
    queryset = StoreProfile.objects.all()
    serializer_class = StoreProfileSerializer


class BuyProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [IsAdminUser | IsOwner]


class StoreProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = StoreProfile.objects.all()
    serializer_class = StoreProfileSerializer
    permission_classes = [IsAdminUser | IsOwner]


@api_view(["POST"])
def login_view(request: HttpRequest) -> Response:
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))


@api_view(["POST"])
def logout_view(request: HttpRequest) -> Response:
    logout(request)
    return Response(status=status.HTTP_200_OK)
