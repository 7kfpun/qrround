# -*- coding: utf-8 -*-
# Django settings for qrround project.
from os import path as op, environ  # , walk, listdir
import logging
import djcelery


SITE_ID = 1

PROJECT_ROOT = op.abspath(op.dirname(op.dirname(__file__)))
PROJECT_NAME = op.basename(PROJECT_ROOT)
PROJECT_NAME = 'QR friends'
SITE_URL = 'http://www.qrfriends.info/'

ENVIRONMENT_NAME = 'core'

DEBUG = True
# TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# COMPRESS_ENABLED = False  # True  # Opposite with DEBUG

RATELIMIT_ENABLE = True

if DEBUG:
    INTERNAL_IPS = '127.0.0.1'
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
        "HIDE_DJANGO_SQL": False,
        "ENABLE_STACKTRACES": True,
    }
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )

AUTH_USER_MODEL = 'qrround.UserClient'

ADMINS = (
    ('123', '123@123.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.  # noqa
        'NAME': 'database.sqlite',                      # Or path to database file if using sqlite3.  # noqa
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.  # noqa
        'PORT': '',                      # Set to empty string for default.
    }
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_PREFIX': '_'.join((PROJECT_NAME, ENVIRONMENT_NAME)),
    }
}
if DEBUG:
    pass
    # CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'  # noqa

CACHE_BACKEND = 'caching.backends.locmem://'

SESSION_COOKIE_AGE = 1209600  # 2 weeks in default

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = True
gettext_noop = lambda s: s
LANGUAGES = (
    ('en', gettext_noop(u'English')),
    ('zh-tw', gettext_noop(u'繁體中文')),
    ('zh-cn', gettext_noop(u'简体中文')),
    ('th', gettext_noop(u'ภาษาไทย')),
    ('ja', gettext_noop(u'日本語')),
)
ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'
ROSETTA_MESSAGES_PER_PAGE = 50

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c((c@5v)q82$+!ko*=3^hg08*zpf38=u*)7tdf80gah=h2p0i7'

RECAPTCHA_PUBLIC_KEY = '6LdQu94SAAAAAAvCQKcPlxSlv4xVH3l66UYDcpMw'
RECAPTCHA_PRIVATE_KEY = '6LdQu94SAAAAAPIbtvEF4qK59iJzsgVd3SxIpnrF'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
)

MIDDLEWARE_CLASSES += 'debug_toolbar.middleware.DebugToolbarMiddleware',

ROOT_URLCONF = 'qrround.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'qrround.wsgi.application'

MEDIA_ROOT = op.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    op.join(PROJECT_ROOT, "static"),
)
FIXTURE_DIRS = (
    op.join(PROJECT_ROOT, 'fixtures/'),
)
TEMPLATE_DIRS = (
    op.join(PROJECT_ROOT, 'templates/'),
)
#for directory_name in walk(PROJECT_ROOT).next()[1]:
#    logging.info(directory_name)
#    directory_path = op.join(PROJECT_ROOT, directory_name)
#    if 'templates' in listdir(directory_path):
#        TEMPLATE_DIRS += (op.join(directory_path, 'templates'),)

INSTALLED_APPS = (
    'redis_cache',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# Applications
INSTALLED_APPS += (
    # Debug
    'debug_toolbar',
    'django_extensions',

    # Contrib
    'django.contrib.admindocs',
    'django.contrib.formtools',
    'djcelery',

    # Community apps
    'captcha',
    'compressor',
    'south',
    'imagekit',
    'rosetta',

    # Qrround
    'qrround',
)

# Celery
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672'
BROKER_URL = 'amqp://guest:guest@ec2-54-245-77-103.us-west-2.compute.amazonaws.com:5672'  # noqa

REDIS_PORT = 37993
REDIS_HOST = "redisdb-710kfpun.dotcloud.com"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

djcelery.setup_loader()

INSTALLED_APPS += ('djcelery',)
CELERY_IMPORTS = ("qrround.views", )

# Mail
EMAIL_HOST_USER = '710kfpun@gmail.com'
EMAIL_HOST_PASSWORD = 'blah blah blah'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
RECEIVE_REGISTRATION = True

# Base apps settings
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d.%m %H:%M:%S',
)

# Override by dotcloud settings
if 'dotcloud' in environ.get('PYTHONPATH', ''):
    from dotcloud import *  # noqa
