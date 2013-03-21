# -*- coding: utf-8 -*-
# Django settings for qrround project.
from os import path as op  # , walk, listdir
import logging
import djcelery


PROJECT_ROOT = op.abspath(op.dirname(op.dirname(__file__)))
PROJECT_NAME = op.basename(PROJECT_ROOT)

ENVIRONMENT_NAME = 'core'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["127.0.0.1"]

COMPRESS_ENABLED = True  # Opposite with DEBUG

RATELIMIT_ENABLE = True

if DEBUG:
    INTERNAL_IPS = '127.0.0.1', '192.168.1.69'
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

SESSION_COOKIE_AGE = 1209600  # 2 weeks in default

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
ugettext = lambda s: s
LANGUAGES = (
    ('en', u'English'),
    ('ja', u'日本語'),
    ('th', u'ภาษาไทย'),
    ('zh-cn', u'简体中文'),
    ('zh-tw', u'繁體中文'),
)

ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = op.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    op.join(PROJECT_ROOT, "static"),
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

FIXTURE_DIRS = (
    op.join(PROJECT_ROOT, 'fixtures/'),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".  # noqa
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    op.join(PROJECT_ROOT, 'templates/'),
)
#for directory_name in walk(PROJECT_ROOT).next()[1]:
#    logging.info(directory_name)
#    directory_path = op.join(PROJECT_ROOT, directory_name)
#    if 'templates' in listdir(directory_path):
#        TEMPLATE_DIRS += (op.join(directory_path, 'templates'),)


INSTALLED_APPS = (
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
    'compressor',
    'south',
    'imagekit',
    'rosetta',

    # Qrround
    'qrround',
)

# Celery
djcelery.setup_loader()
CELERY_ENABLED = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
BROKER_URL = 'amqp://nyezagug:DSBH7ibcP4BeNVfObtTj4hgDvlM6LQgT@tiger.cloudamqp.com/nyezagug'  # noqa
INSTALLED_APPS += ('djcelery',)
CELERY_IMPORTS = ("qrround.views", )

# Mail
EMAIL_HOST_USER = '7kfpun@gmail.com'
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
