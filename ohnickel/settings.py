"""
Django settings for songisode project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a5s%y@^a)rmd+^5-aay6qv!oi7qv04j+2+04)4y0fh6f!^-a$t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "templates/static"),

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    "social_auth.context_processors.social_auth_by_type_backends"
)

ALLOWED_HOSTS = []

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/login-error/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ohnickel',
    #'south',
    #'rest_framework',
    'social_auth',
    #'djcelery',                 # Add Django Celery
    #'kombu.transport.django',
    #'django_bitcoin',
)

AUTHENTICATION_BACKENDS = (
  'social_auth.backends.twitter.TwitterBackend',
  'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ohnickel.middleware.authentication.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#SOCIAL_AUTH_USER_MODEL = 'ohnickel.User'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 17
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16

SOCIAL_AUTH_PIPELINE_RESUME_ENTRY = 'social_auth.backends.pipeline.misc.save_status_to_session'
SOCIAL_AUTH_PARTIAL_PIPELINE_KEY = 'partial_pipeline'


TWITTER_CONSUMER_KEY         = 'LjdgXhqPHbyeDMO47qtfow'
TWITTER_CONSUMER_SECRET      = 'ECit0NyT6dtXbHylU3UB3S1PPlQM1LfrceyljhRs'

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter',)

ROOT_URLCONF = 'ohnickel.urls'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = 'ohnickel.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BOT_EMAIL = 'steamtradebot1@gmail.com'
BOT_EMAIL_PASSWORD = 'shabotlol1'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = BOT_EMAIL
EMAIL_HOST_PASSWORD = BOT_EMAIL_PASSWORD



STATIC_URL = '/static/'
BROKER_URL = 'django://'

BITCOIND_CONNECTION_STRING = "http://e9d916d9-d773-44db-a6c3-2a69206e8814:shahexlol1234@rpc.blockchain.info:80"
BITCOIN_MINIMUM_CONFIRMATIONS = 1

