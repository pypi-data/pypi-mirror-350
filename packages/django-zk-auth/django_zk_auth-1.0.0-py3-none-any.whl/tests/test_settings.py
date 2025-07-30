# tests/test_settings.py
import os
from pathlib import Path
import django
import pytest
# Base directory for your tests or project root - adjust as needed
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key-for-tests"

INSTALLED_APPS = [
    "django.contrib.contenttypes",  # minimal app to satisfy Django internals
    'django.contrib.auth',
    'django.contrib.sessions',
    'django_zk_auth', 
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # in-memory SQLite DB, no files needed
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",  # unique name for the in-memory cache
    }
}

AUTHENTICATION_BACKENDS = [
    'django_zk_auth.auth_backend.ZKAdminAuthenticationBackend',      # for admin login
    'django_zk_auth.auth_backend.ZKAuthenticationBackend',           # for user login
    'django_zk_auth.auth_backend.ZKPasswordlessBackend',             # for registration or other flows
    'django.contrib.auth.backends.ModelBackend',                     # fallback to standard auth (optional)
]

# Optional but recommended for testing speed & simplicity:
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Add other minimal settings if needed, e.g.:
USE_TZ = True
TIME_ZONE = "UTC"
DEBUG = True

AUTH_USER_MODEL = 'django_zk_auth.ZKUser' 