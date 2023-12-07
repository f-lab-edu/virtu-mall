from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(verbose_name="유저 이름", max_length=20, null=False)
    address = models.CharField(verbose_name="유저 주소", max_length=200, null=False)
    phone = models.CharField(verbose_name="유저 전화번호", max_length=11, null=False)
    email = models.EmailField(verbose_name="유저 이메일", null=False)
    is_staff = models.BooleanField(verbose_name="스태프 여부", default=False)
    created_at = models.DateTimeField(verbose_name="유저 정보 생성시간", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="유저 정보 수정 시간", auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "user"
