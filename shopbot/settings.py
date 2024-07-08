import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT = "https://www.limoo.ai/"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u3(hg*ch^cjnx4o(7d(!*d+%r5fd$1bfenaq%j9dwszrpt718c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.93.231.240', 'limoo.ai', 'www.limoo.ai']

from datetime import timedelta
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'main',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'dj_rest_auth',
    'django_rest_passwordreset',
    'openai',
    'ckeditor',
    'django.forms',
    "rest_framework_simple_api_key",
    "ApiService"
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True   
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

ROOT_URLCONF = 'shopbot.urls'
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'shopbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Actual directory user files go to
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL used to access the media
MEDIA_URL = '/media/'
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT  = os.path.join(BASE_DIR, 'static')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ali.sharafi85@gmail.com'
EMAIL_HOST_PASSWORD = 'S8aVrQjUYJODxI5B'

'''

EMAIL_BACKEND = 'django_imap_backend.ImapBackend'
EMAIL_IMAP_SECRETS = [
    {
        'HOST': 'smtp.gmail.com',
        'PORT': 587,  # default 143 and for SSL 993
        'USER': 'armansaheb94@gmail.com',
        'PASSWORD': 'gnuyumaspsxgvhel',
        'MAILBOX': 'limoo',  # Created if not exists
        'SSL': True  # Default
    }
]
'''

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', 
    )
}
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_BASEPATH = os.path.join(BASE_DIR, 'static/ckeditor/ckeditor/')

CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',

    },
}
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MyCustomCKEditorWidget(CKEditorUploadingWidget):
   template_name = "templates/widget.html"


SIMPLE_API_KEY = {
    "FERNET_SECRET": "QG-heVovSsExvMqgRd6jwvwq6tL7ImPmMOVxiPVWXzQ=",
    "API_KEY_LIFETIME": 365,
    "AUTHENTICATION_KEYWORD_HEADER": "Api-Key",
    "ROTATION_PERIOD": timedelta(days=7),
    "ROTATION_FERNET_SECRET": ""
}
