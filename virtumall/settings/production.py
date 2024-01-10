from .base import *

DEBUG = False

ALLOWED_HOSTS = ["http://ec2-15-164-50-94.ap-northeast-2.compute.amazonaws.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
    },
}
