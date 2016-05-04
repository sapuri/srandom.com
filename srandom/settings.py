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
SECRET_KEY = '!xw174_49f)d8llpm8)k3k-azlak^y)fi@y^ami_x2f(3es6%q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',                       # django-bootstrap3
    'social.apps.django_app.default',   # python-social-auth
    'debug_toolbar',                    # django-debug-toolbar
    'main.apps.MainConfig',             # Main
    'users.apps.UsersConfig',           # Users
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django-htmlmin
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'srandom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # python-social-auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'srandom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'srandom',
        'USER': 'sysco',
        'PASSWORD': 'm3imsWM8JcBM',
        'HOST': '',
    }
}


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# サーバー時はON
# STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATIC_URL = '/static/'

# ローカル時はON
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# メッセージ設定
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# ログインせずに @login_required ページにアクセスしたら飛ばす
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

# django-bootstrap3
BOOTSTRAP3 = {
    'css_url':'/static/css/bootstrap.min.css'
}


# python-social-auth
AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_TWITTER_KEY    = 'Pwyx6QZgunJsbrArLub7pNKwu'
SOCIAL_AUTH_TWITTER_SECRET = 'D7J4xAE7aXLrqGyaKy8adpxtU1rrAEuZy8MaRUw3GUUzG6BLeO'


# django-htmlmin
HTML_MINIFY = False
