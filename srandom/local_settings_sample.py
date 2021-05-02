# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<SECRET_KEY>'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<NAME>',
        'USER': '<USER>',
        'PASSWORD': '<PASSWORD>',
        'HOST': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


# python-social-auth
SOCIAL_AUTH_TWITTER_KEY = '<SOCIAL_AUTH_TWITTER_KEY>'
SOCIAL_AUTH_TWITTER_SECRET = '<SOCIAL_AUTH_TWITTER_SECRET>'
