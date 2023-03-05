"""Test settings for Easystart project."""

from .settings import *  # noqa

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# Wrap all requests funtions with transaction.atomic
DATABASES["default"]["ATOMIC_REQUESTS"] = True

RUN_TEST = True
