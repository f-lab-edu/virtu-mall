from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "CONN_MAX_AGE": 30,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}

CSRF_TRUSTED_ORIGINS = [
    "http://http://ec2-3-38-119-238.ap-northeast-2.compute.amazonaws.com/",
]

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_HOST = "s3.ap-northeast-2.amazonaws.com"
AWS_QUERYSTRING_AUTH = False

MEDIAFILES_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"
DEFAULT_FILE_STORAGE = "utils.asset_storage.MediaStorage"

STATICFILES_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
STATICFILES_STORAGE = "utils.asset_storage.StaticStorage"
