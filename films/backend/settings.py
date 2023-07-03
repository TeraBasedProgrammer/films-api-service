from datetime import timedelta
from pathlib import Path
import os
import secrets

import boto3

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))

DEBUG = os.environ.get("DEBUG", "False").lower() == 'true'

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", 'localhost').split(", ")

# Remote AWS host
REMOTE_HOST = ALLOWED_HOSTS[-1]

REMOTE_SCHEME = 'https'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_extra_fields',
    'django_filters',
    'rest_framework_simplejwt',

    # Current project apps
    'actors',
    'films',
    'playlists',
    'authorization',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authorization.middleware.NoCredentialsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
   "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get('SQL_PASSWORD'), # if DEBUG else os.environ.get("SQL_PROD_PASSWORD"),
        "HOST": os.environ.get('SQL_HOST'), # if DEBUG else os.environ.get("SQL_PROD_HOST"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# Actual directory user files go to
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL used to access the media
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'errors',
    'DEFAULT_PAGINATION_CLASS': 'films.paginators.CustomPageSizePagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'authorization.permissions.CustomIsAuthenticated',
    ],
}

# JWT auth settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'SIGNING_KEY': secrets.token_hex(32),
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ("rest_framework_simplejwt.tokens.AccessToken",),
}

if not os.environ.get('ACCESS_KEY') or not os.environ.get('AWS_SECRET_KEY'):
    AWS_SESSION = boto3.Session()
else:
    AWS_SESSION = boto3.Session(
        aws_access_key_id=os.environ.get('ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    )

DJANGO_LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] [{asctime}] [{module}.{funcName}]: {message}",
            "datefmt": "%y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "logger": {
            "handlers": ["console"],
            "propagate": True,
            "level": DJANGO_LOG_LEVEL,
        },
    },
}



