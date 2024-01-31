from .base import *

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
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}


AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

DEFAULT_FILE_STORAGE = "utils.asset_storage.MediaStorage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
STATICFILES_LOCATION = "static"
MEDIAFILES_LOCATION = "media"
