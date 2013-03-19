from settings import *  # noqa


ENVIRONMENT_NAME = "test"

# Databases
DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = ':memory:'

# Caches
CACHES['default']['BACKEND'] = 'django.core.cache.backends.locmem.LocMemCache'
CACHES['default']['KEY_PREFIX'] = '_'.join((PROJECT_NAME, ENVIRONMENT_NAME))

INSTALLED_APPS += 'lettuce.django',

LETTUCE_AVOID_APPS = (
    'coffin',
    'compressor',
    'dajax',
    'dajaxice',
    'debug_toolbar',
    'django_gevent_deploy',
    'django_nose',
    'djcelery',
    'passwords',
    'south',
    'tastypie',
)

SOUTH_TESTS_MIGRATE = True
logging.info('Integration test settings loaded.')
