# Django settings for hellodjango project.
from qrround.settings.settings import *
import json


SECRET_KEY = 'sb4=y4x8kkn&amp;j94%oe0x6)b!9)w7bl#7%9u8g6uva0mgw^l%ul'
with open('/home/dotcloud/environment.json') as f:
  env = json.load(f)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
# …
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'happydb',
        'USER': env['DOTCLOUD_DB_SQL_LOGIN'],
        'PASSWORD': env['DOTCLOUD_DB_SQL_PASSWORD'],
        'HOST': env['DOTCLOUD_DB_SQL_HOST'],
        'PORT': int(env['DOTCLOUD_DB_SQL_PORT']),
    }
}

