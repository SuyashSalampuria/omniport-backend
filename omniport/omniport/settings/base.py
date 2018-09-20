"""
Django settings for omniport project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from discovery.discovery import Discovery

# The location of this file
FILE_PATH = os.path.abspath(__file__)

# The 'settings' package, inside the 'omniport' directory
SETTINGS_DIR = os.path.dirname(FILE_PATH)

# The 'omniport' package, inside the base directory
OMNIPORT_DIR = os.path.dirname(SETTINGS_DIR)

# The project directory, inside which the project code rests
PROJECT_DIR = os.path.dirname(OMNIPORT_DIR)

# Tha parent directory inside which the project directory rests
PARENT_DIR = os.path.dirname(PROJECT_DIR)

# The 'configuration' directory where all settings will be loaded from
CONFIGURATION_DIR = os.path.join(PARENT_DIR, 'configuration')

# The 'branding' directory where all branding imagery will be loaded from
BRANDING_DIR = os.path.join(PARENT_DIR, 'branding')

# The 'static' directory where all static files will be collected into
STATIC_DIR = os.path.join(PARENT_DIR, 'static_files')

# The 'media' directory where all uploaded media will be stored in
MEDIA_DIR = os.path.join(PARENT_DIR, 'media_files')

# The 'core' directory where all Omniport core apps will be loaded from
CORE_DIR = os.path.join(PROJECT_DIR, 'core')

# The 'services' directory where all Omniport service apps will be loaded from
SERVICES_DIR = os.path.join(PROJECT_DIR, 'services')

# The 'apps' directory where all Omniport drop-in apps will be loaded from
APPS_DIR = os.path.join(PROJECT_DIR, 'apps')

# Application declarations
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # PyPI packages
    'rest_framework',
    'channels',
    'django_countries',
    'django_filters',
    'easy_select2',
    'nested_admin',
    'corsheaders',

    # Core apps
    'kernel',
    'session_auth',
    'token_auth',
]

# Check if shell present and if yes, add to INSTALLED_APPS
SHELL_PRESENT = False
try:
    from shell.apps import ShellConfig

    SHELL_PRESENT = True
    INSTALLED_APPS.append(
        'shell.apps.ShellConfig',
    )
except ImportError:
    # Shell has not been installed
    pass

# Discovery

DISCOVERY = Discovery(SERVICES_DIR, APPS_DIR)
DISCOVERY.discover()

DISCOVERY.prepare_installed_apps()

INSTALLED_APPS += DISCOVERY.service_installed_apps

INSTALLED_APPS += DISCOVERY.app_installed_apps

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'omniport.middleware.drf_auth.DrfAuth',

    'omniport.middleware.ip_address_rings.IpAddressRings',
    'omniport.middleware.person_roles.PersonRoles',
]

ROOT_URLCONF = 'omniport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
            os.path.join(OMNIPORT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'omniport.context.branding.branding_imagery',
                'omniport.context.branding.branding_text',
                'omniport.context.site.site_information',
            ],
        },
    },
]

# Authentication

AUTH_USER_MODEL = 'kernel.User'

AUTHENTICATION_BACKENDS = [
    'kernel.auth_backends.generalised.GeneralisedAuthBackend',
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

# Session store

SESSION_ENGINE = 'redis_sessions.session'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True

# REST framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# Static files

STATICFILES_DIRS = [
    os.path.join(OMNIPORT_DIR, 'static'),
]

STATIC_URL = '/static/'

STATIC_ROOT = STATIC_DIR

# Branding files

BRANDING_URL = '/branding/'

BRANDING_ROOT = BRANDING_DIR

# Media files

MEDIA_URL = '/media/'

MEDIA_ROOT = MEDIA_DIR

# WSGI application served by Gunicorn
WSGI_APPLICATION = 'omniport.wsgi.application'

# ASGI application served by Daphne
ASGI_APPLICATION = 'omniport.routing.application'

# Swapper models
try:
    if SHELL_PRESENT:
        from shell.swapper import *
except ImportError:
    # Will never enter this block because of the SHELL_PRESENT check
    pass

# Roles
ROLES = list()
