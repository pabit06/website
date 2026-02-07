"""
Django settings for Bhanjyang Cooperative website.
"""
import os
import sys
from pathlib import Path

# Optional: load .env for local development (pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-in-production-bhanjyang-coop',
)

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1')

# Comma-separated in production, e.g. bhanjyang.coop.np,www.bhanjyang.coop.np
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,192.168.1.156').split(',')
    if h.strip()
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'apps.home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Project-level static (root). App static: apps/home/static/
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Use in-memory SQLite only when running tests (project has no DB in dev)
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
