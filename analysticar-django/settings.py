"""
Django settings for analysticar project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ibmclouddb',                                   # Or path to database file if using sqlite3.
        'USER': 'ibm_cloud_d2bc9c2b_1364_4764_93df_cc369faec116',                                     # Not used with sqlite3.
        'PASSWORD': '695c7878f51ddc5efceaf683db523a9cc739074ed14516c8b3f6f5061f762ecc',                      # Not used with sqlite3.
        'HOST': '500aaa93-4b2a-4c61-92b5-d4d5932aadb0.0135ec03d5bf43b196433793c98e8bd5.databases.appdomain.cloud',       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '31481',                                     # Set to empty string for default. Not used with sqlite3.
    }
}
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b0=n&i9@8ah-fkyqrusyd(%_wnyw%9vm0@kj@^i7tozuyh*b8+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analysticar',
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

ROOT_URLCONF = 'analysticar-django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.csrf',
            ],
        },
    },
]

WSGI_APPLICATION = 'analysticar-django.wsgi.application'


AUTH_USER_MODEL = 'analysticar.User'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Directorio de templates y de statics.

STATICFILES_DIRS= [os.path.join(BASE_DIR,'static')]



LOGGING = {
     'version': 1,
     'disable_existing_loggers': False,
     'formatters': {
         'ourFormatter': {
             'format': '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
             'datefmt': '%m/%d/%Y %I:%M:%S',
         },
     },
     'handlers': {
         'theConsole': {
             'class': 'logging.StreamHandler',
             'formatter': 'ourFormatter',        
         },
     },
     'root': {
         'level': 'DEBUG',
         'handlers': ['theConsole'],
     },
}

LOGIN_URL = '/iniciar-sesion/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'smarticket.suport@gmail.com'
EMAIL_HOST_PASSWORD = 'asd123asd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Analyticar'