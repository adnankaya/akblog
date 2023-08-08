from .base import *

STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


DEBUG = False

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'INFO',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'INFO'
        },
        'django.request': {  # logging 500 errors to database
            'handlers': ['db_log',],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

