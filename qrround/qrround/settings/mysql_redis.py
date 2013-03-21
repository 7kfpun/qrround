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


CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        'KEY_PREFIX': '_'.join((PROJECT_NAME, ENVIRONMENT_NAME)),
        "LOCATION": "127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

