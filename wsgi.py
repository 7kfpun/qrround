import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'qrround')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'qrround.settings.dotcloud'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
