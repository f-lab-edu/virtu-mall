from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "virtumall",
        "USER": "root",
        "PASSWORD": "virtumall1225",
        "HOST": "mysql",
        "PORT": "3306",
    },
}
