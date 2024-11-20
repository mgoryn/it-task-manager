from .base import *
import os

DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"

ALLOWED_HOSTS = ["127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
