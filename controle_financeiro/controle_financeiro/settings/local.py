import os
from decouple import config
from .base import *


SETTING_NAME = "local"

ROOT_URLCONF = "controle_financeiro.urls.local"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

# MIDDLEWARE += [
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
# ]

# INSTALLED_APPS += ["debug_toolbar"]

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
