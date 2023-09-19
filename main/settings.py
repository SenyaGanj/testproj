"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from .config_utils import get_option, string_as_bool, list_of_strings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_option('common', 'SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_option('common', 'DEBUG', True, string_as_bool)

ALLOWED_HOSTS = get_option(
    'common',
    'ALLOWED_HOSTS',
    'localhost, localhost:8000, django, django:8000, 127.0.0.1, 127.0.0.1:8000',
    list_of_strings
)

CSRF_TRUSTED_ORIGINS = get_option(
    'common',
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost, http://localhost:8000, http://django, http://django:8000, http://127.0.0.1, http://127.0.0.1:8000',
    list_of_strings
)

CORS_ORIGIN_WHITELIST = get_option('common', 'CORS_ORIGIN_WHITELIST', '', list_of_strings)
CORS_EXPOSE_HEADERS = ('Content-Type', 'X-CSRFToken')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = (
    'accounts.apps.AccountsConfig',
    'fileman.apps.FilemanConfig',
)

INSTALLED_APPS += PROJECT_APPS

THIRD_PARTY_APPS = (
    'corsheaders',
    'rest_framework',
    'django_celery_beat',
)

INSTALLED_APPS += THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_option('database', 'BACKEND', 'django.db.backends.sqlite3'),
        'NAME': get_option('database', 'NAME', BASE_DIR / 'db.sqlite3'),
        'USER': get_option('database', 'USER', ''),
        'PASSWORD': get_option('database', 'PASSWORD', ''),
        'HOST': get_option('database', 'HOST', ''),
        'PORT': get_option('database', 'PORT', 5432, int),
        # https://docs.djangoproject.com/en/3.1/ref/databases/#transaction-pooling-and-server-side-cursors
        'DISABLE_SERVER_SIDE_CURSORS': get_option('database', 'DISABLE_SERVER_SIDE_CURSORS', False, string_as_bool),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            # 'client_encoding': 'utf8'
        },
        'TEST': {
            'NAME': f'test_projtest',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = get_option('common', 'static_root', BASE_DIR / 'static')
STATIC_URL = get_option('common', 'static_url', '/backend_static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = get_option('common', 'media_root', BASE_DIR / 'media')
MEDIA_URL = get_option('common', 'media_url', '/media/')

AUTH_USER_MODEL = 'accounts.User'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_option('email', 'HOST', 'smtp.mail.ru')
EMAIL_HOST_USER = get_option('email', 'HOST_USER', '')
EMAIL_HOST_PASSWORD = get_option('email', 'HOST_USER', '')
EMAIL_PORT = get_option('email', 'PORT', 2525, int)
EMAIL_USE_TLS = get_option('email', 'USE_TLS', True, string_as_bool)
EMAIL_USE_SSL = get_option('email', 'USE_SSL', False, string_as_bool)
SERVER_EMAIL = get_option('email', 'SERVER_EMAIL', '')
DEFAULT_FROM_EMAIL = get_option('email', 'DEFAULT_FROM_EMAIL', '')


CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_TASK_IGNORE_RESULT = True
CELERYD_TIME_LIMIT = 50
CELERY_BEAT_SCHEDULE = {
    'check_new_files': {
        'task': 'fileman.tasks.check_new_files',
        'schedule': timedelta(seconds=20),
    },
}

CELERY_BROKER_URL = get_option('celery', 'BROKER_URL', 'redis://redis:6379/0')
CELERY_TASK_SOFT_TIME_LIMIT = get_option('celery', 'TASK_SOFT_TIME_LIMIT', 60, int)
CELERY_TASK_TIME_LIMIT = get_option('celery', 'TASK_SOFT_TIME_LIMIT', 90, int)
