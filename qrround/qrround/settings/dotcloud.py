import json
with open('/home/dotcloud/environment.json') as f:
    env = json.load(f)

DEBUG = False
ALLOWED_HOSTS = ['qrround-710kfpun.dotcloud.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qrround',
        'USER': env['DOTCLOUD_DB_MYSQL_LOGIN'],
        'PASSWORD': env['DOTCLOUD_DB_MYSQL_PASSWORD'],
        'HOST': env['DOTCLOUD_DB_MYSQL_HOST'],
        'PORT': int(env['DOTCLOUD_DB_MYSQL_PORT']),
    }
}

USE_REDIS = False
if USE_REDIS:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': env['DOTCLOUD_CACHE_REDIS_HOST']+':'+env['DOTCLOUD_CACHE_REDIS_PORT'],  # noqa
            'OPTIONS': {
                'DB': 1,
                'PASSWORD': env['DOTCLOUD_CACHE_REDIS_PASSWORD'],
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            },
        },
    }

    # we also are going to use redis for our session cache as well.
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# BROKER_URL = 'amqp://nyezagug:DSBH7ibcP4BeNVfObtTj4hgDvlM6LQgT@tiger.cloudamqp.com/nyezagug'  # noqa
BROKER_URL = 'amqp://tiyleaba:nGub3yv4ik7VYrOqut1IIoaNHgwhEUfU@bunny.cloudamqp.com/tiyleaba'  # noqa
# BROKER_URL = 'amqp://cmvunnej:gGXlI_n5rh6FE-Nsd6ILNru2loUAT0-F@tiger.cloudamqp.com/cmvunnej'  # noqa
BROKER_URL = 'amqp://guest:guest@ec2-54-245-77-103.us-west-2.compute.amazonaws.com:5672'  # noqa

# media settings
MEDIA_ROOT = '/home/dotcloud/data/media/'
MEDIA_URL = '/media/'

# static settings
STATIC_ROOT = '/home/dotcloud/volatile/static/'
STATIC_URL = '/static/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'  # noqa
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/supervisor/blogapp.log',
            'maxBytes': 1024*1024*25,  # 25 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
