import os
import ssl
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(" ")

SITE_ID = 1

# Application definition

DEFAULT_DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
]


PROJECT_APPS = [
    'apps.core',
    'apps.home',
    'apps.users',
    'apps.post',
    'apps.general',
    'apps.aboutus',
    'apps.courses',
    'apps.categories',
    'apps.developers',
]
THIRD_PARTY_APPS = [
    'django_extensions',
    'taggit',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'phonenumber_field',
    'django_cleanup',
    'django_db_logger',
    'ckeditor',
]
# Application definition
INSTALLED_APPS = DEFAULT_DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

AUTH_USER_MODEL = 'users.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #  internal
    'apps.core.middlewares.ForceDefaultLanguageMiddleware',
    #  django
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #  internals
    'apps.core.middlewares.metric_middleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # internals
                'apps.core.context_processors.google_tag_manager',

            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_SLUG = os.environ.get("DB_SLUG", "sqlite")

if DB_SLUG == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USERNAME'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }
elif DB_SLUG == "sqlite":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True
USE_TZ = True


LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('tr', _('Turkish')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = "users:login"

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticroot"
# STATICFILES_DIRS is the list of folders where Django will search for 
#   additional static files aside from the static folder of each app installed.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True
# phone number
PHONENUMBER_DEFAULT_REGION = "TR"

#  Post
MAX_POST_IMAGES_LEN = int(os.environ.get("MAX_POST_IMAGES_LEN", 5))
POST_LIMIT_PER_PAGE = int(os.environ.get("POST_LIMIT_PER_PAGE", 12))
COURSE_LIMIT_PER_PAGE = int(os.environ.get("COURSE_LIMIT_PER_PAGE", 12))
DEVELOPERS_LIMIT_PER_PAGE = int(os.environ.get("DEVELOPERS_LIMIT_PER_PAGE", 20))
MAX_DEVELOPERS_SKILLS_NUMBER = int(os.environ.get("MAX_DEVELOPERS_SKILLS_NUMBER", 10))
COUNT_MOST_USED_TAGS = int(os.environ.get("COUNT_MOST_USED_TAGS", 10))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
#  Redis
# REDIS_USERNAME = os.environ.get('REDIS_USERNAME')
# REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
# REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
# REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
# REDIS_DB_NUM = os.environ.get('REDIS_DB_NUM', '0')

# PARAMS_CELERY = {}
# if REDIS_USERNAME and REDIS_PASSWORD:
#     # for secure connection use rediss://
#     CELERY_BROKER_URL = f'rediss://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'
#     CELERY_RESULT_BACKEND = f'rediss://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'
#     CELERY_REDIS_BACKEND_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}
#     BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}

#     PARAMS_CELERY.update({
#         "broker_use_ssl":{"ssl_cert_reqs": ssl.CERT_NONE},
#         "redis_backend_use_ssl":{"ssl_cert_reqs": ssl.CERT_NONE},
#     })
# else:
#     CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'
#     CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": CELERY_RESULT_BACKEND,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }
# Cache time to live is 2 minutes.
DEFAULT_CACHE_TTL = 60 * 2
TTL_1_MINUTE = 60*1
TTL_2_MINUTE = 60*2
TTL_3_MINUTE = 60*3
TTL_4_MINUTE = 60*4
TTL_5_MINUTE = 60*5
TTL_10_MINUTE = 60*10
TTL_15_MINUTE = 60*15
TTL_20_MINUTE = 60*20
TTL_1_HOUR = 60*60
TTL_1_DAY = 60*60*24
TTL_1_WEEK = 60*60*24*7
# prefixes
KEY_PREFIX_POST_INDEX = "post_index_"
KEY_PREFIX_POST_DETAIL = "post_detail_"
KEY_PREFIX_USER_COUNT = "user_count_"



############## CKEDITOR ##############
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_MyCustomToolbar': [
            {'name': 'basic', 'items': [
                'Source',
                '-',
                'Bold','Italic','Underline', 'Strike',
            ]},
            {'name': 'code', 'items': [
                'CodeSnippet',  # add the codesnippet button name
                'CodeSnippet',  # add the codesnippet button name
                'CodeSnippet',  # add the codesnippet button name
            ]},
            {'name': 'insert',
             'items': ['Image', 'Table', 'Iframe']},
            '/',
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',]},
        ],
        'codeSnippet_theme': 'github',
        # uncomment to restrict only those languages
        'codeSnippet_languages': {
            'python': 'Python',
            'javascript': 'Javascript',
            'yaml': 'yaml',
            'bash': 'bash',
            'css': 'css',
            'html': 'html',
        },
        'toolbar': 'MyCustomToolbar',
        'extraPlugins': ','.join(
            [
                # add the follow plugins
                'codesnippet',
                'widget',
                'dialog',
                'uploadimage', # the upload image feature
            ]),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
CONTACT_FROM_EMAIL = os.environ.get('CONTACT_FROM_EMAIL')