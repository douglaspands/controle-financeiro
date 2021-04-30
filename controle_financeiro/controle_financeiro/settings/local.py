import os
from decouple import config
from .base import *


SETTING_NAME = "local"

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
    ("css", os.path.join(BASE_DIR, "static", "css")),
    ("font", os.path.join(BASE_DIR, "static", "font")),
    ("icon", os.path.join(BASE_DIR, "static", "icon")),
    ("img", os.path.join(BASE_DIR, "static", "img")),
    ("js", os.path.join(BASE_DIR, "static", "js")),
    ("vendor", os.path.join(BASE_DIR, "static", "vendor")),
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
