from pathlib import Path
import os
# import mongoengine

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-dev-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'visiters',
    'rest_framework',
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MainWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'visiters.helper.task_count'
            ],
        },
    },
]

WSGI_APPLICATION = 'MainWeb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


import dj_database_url

# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600)
# }

DATABASES = {
  'default': dj_database_url.config(conn_max_age=600)
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mssql",
#         "NAME": "sql6440533",
#         "USER": "sql6440533",
#         "PASSWORD": "cjhzrliSFZ",
#         "HOST": "sql6.freemysqlhosting.net",
#         "PORT": "3306",
#     },
# }

# DATABASE = {
#     'default': {
#         'ENGINE': 'djongo',
#         "NAME": "Droid7",
#         'ENFORCE_SCHEMA': False,
#         "CLIENT": {
#             "host": "mongodb+srv://root:root@cluster0.m1lzw.mongodb.net/Droid7?retryWrites=true&w=majority",
#         },
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "vizit",
#         "USER": "root",
#         "PASSWORD": "root",
#         "HOST": "localhost",
#         "PORT": "3306",
#     },
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')