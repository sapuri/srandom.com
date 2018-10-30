"""
Django settings for srandom project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Load SECRET_KEY from local_settings.py

# SECURITY WARNING: don't run with debug turned on in production!
# Load DEBUG from local_settings.py
DEBUG = False

# Load ALLOWED_HOSTS from local_settings.py


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',                    # django-debug-toolbar
    'bootstrap3',                       # django-bootstrap3
    'social_django',                    # python-social-auth
    'compressor',                       # django-compressor
    'maintenance_mode',                 # django-maintenance-mode
    'sslserver',                        # django-sslserver
    'main.apps.MainConfig',             # Main
    'users.apps.UsersConfig',           # Users
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django-debug-toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # django-htmlmin
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    # django-maintenance-mode
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'srandom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # python-social-auth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'srandom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Load DATABASES from local_settings.py


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Load all local settings
try:
    from .local_settings import *
except ImportError:
    pass


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# メッセージ設定
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# ログインせずに @login_required ページにアクセスしたら飛ばす
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'


# django-debug-toolbar
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']


# django-bootstrap3
BOOTSTRAP3 = {
    'css_url': '/static/css/bootstrap.min.css'
}


# python-social-auth
AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
]

# Load SOCIAL_AUTH_TWITTER_KEY from local_settings.py
# Load SOCIAL_AUTH_TWITTER_SECRET from local_settings.py


# django-compressor
# DEBUG と反対の値になるため通常は指定する必要無し
# COMPRESS_ENABLED = True

# django-htmlmin
# DEBUG と反対の値になるため通常は指定する必要無し
# HTML_MINIFY = True

# django-maintenance-mode
MAINTENANCE_MODE_IGNORE_SUPERUSER = True


if not DEBUG:
    # Travis CI
    if 'TRAVIS' in os.environ:
        SECRET_KEY = 'mj8f0l0)noi_7#l(+t9f8az72$)v+icvf6^87v6847!osel6+d'
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'travis_ci',
                'USER': 'root',
                'PASSWORD': '',
                'HOST': '',
                'OPTIONS': {
                    'charset': 'utf8mb4',
                },
            }
        }
