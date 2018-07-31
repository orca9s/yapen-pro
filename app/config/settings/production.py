import sys

from .base import *

secrets = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))
# Django가 runserver로 켜졌는지 확인
RUNSERVER = 'runserver' in sys.argv
DEBUG = False
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']
# runserver로 production환경을 실행할 경우
if RUNSERVER:
    DEBUG = True
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
    ]

WSGI_APPLICATION = 'config.wsgi.production.application'
INSTALLED_APPS += [
    'storages',
]

# DB
DATABASES = secrets['DATABASES']

# Media
DEFAULT_FILE_STORAGE = 'config.storages.S3DefaultStorage'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']

# Log
# 존재할 경우 그냥 쓰도록
LOG_DIR = '/var/log/django'
# 존재하지 않으면 생성
if not os.path.exists(LOG_DIR):
    # ROOT_DIR/.log를 쓰자
    LOG_DIR = os.path.join(ROOT_DIR, '.log')
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'django.server',
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10485760,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_error'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
