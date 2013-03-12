from settings import *
import os


# CREATE DATABASE qrround CHARACTER SET utf8;
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.  # noqa
        'OPTIONS': {
            'read_default_file': os.path.join(PROJECT_ROOT, 'settings/my.cnf'),
        },
    }
}

## Caches
#CACHES = {
#    'default': {
#    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#    'KEY_PREFIX': '_'.join((PROJECT_NAME, ENVIRONMENT_NAME))
#    }
#}
