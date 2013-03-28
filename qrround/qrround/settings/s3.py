from settings import *


INSTALLED_APPS += (
    'storages',
    's3_folder_storage',
)

DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"
# STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
# STATIC_S3_PATH = "static"
AWS_ACCESS_KEY_ID = 'AKIAJ5UUNYBEDJPAISNQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'qrround'

MEDIA_ROOT = '/%s' % DEFAULT_S3_PATH
MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
# STATIC_ROOT = "/%s/" % STATIC_S3_PATH
# STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
