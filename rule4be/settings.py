from pathlib import Path
import dj_database_url
import datetime
import os
import logging
import environ
import logging.config
from django.core.mail.backends.console import EmailBackend
from dotenv import load_dotenv

env = environ.Env()
environ.Env.read_env()  # Reads .env file

# Example usage
DEBUG = env.bool('DEBUG', default=False)


load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'rule4be-fc4445b7e11b.herokuapp.com',
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    'rule4.app',
    '192.168.68.120',
    '41.13.133.59',  # IP Address South Africa
    '35.242.172.181',  # IP Address GKE LB
]

CSRF_TRUSTED_ORIGINS = [
    'https://rule4.app',
    'http://localhost:8000',
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'whitenoise',
    'storages',
    "snapshots",
    "rule4be",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
# Redirect URLs after login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


ROOT_URLCONF = "rule4be.urls"

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         # Adjust 'templates' if your directory structure is different
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = "rule4be.wsgi.application"

development = os.environ.get('DEVELOPMENT')

if development:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,  # Timeout in seconds
            },
        }
    }
else:

    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

############################################
#  AWS S3 settings
############################################


# This is still needed for the collectstatic command to know where to find static files locally
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Adjust the path as necessary
]
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USE_S3 = os.environ.get('USE_S3')

if USE_S3 == 'True':
    # AWS S3 settings for static files
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    # Change if your bucket is in a different region
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get(
        'AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_QUERYSTRING_EXPIRE = 3600

    # S3 static settings
    AWS_LOCATION = 'static'
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # S3 media settings
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# Email settings
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
# e.g., email.us-east-1.amazonaws.com
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

# Optional settings
# (default; safety factor applied to rate limits to stay below the AWS SES maximum send rate)
AWS_SES_AUTO_THROTTLE = 0.5
DEFAULT_FROM_EMAIL = 'info@rule4.app'

############################################################
# AWS CloudFront Settings
############################################################

AWS_CLOUDFRONT_KEY = env.str(
    'AWS_CLOUDFRONT_KEY', multiline=True).encode('ascii').strip()
AWS_CLOUDFRONT_KEY_ID = env.str('AWS_CLOUDFRONT_KEY_ID').strip()


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://rule4-943c9feeb754.herokuapp.com",
    "https://rule4.app",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

JWT_AUTH = {
    # Change this to a secure, secret key.
    'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
    'JWT_ALGORITHM': os.environ.get('JWT_ALGORITHM'),
    'JWT_ALLOW_REFRESH': True,
    # Adjust the token expiration time as needed.
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}


# # Configure logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'myapp.custom_email_logger': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }

# # Apply logging configuration
# logging.config.dictConfig(LOGGING)

# # Define a logger for custom email sending
# logger = logging.getLogger('rule4be.custom_email_logger')
