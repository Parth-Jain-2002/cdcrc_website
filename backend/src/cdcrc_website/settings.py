"""
Django settings for cdcrc_website project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
from dotenv import load_dotenv
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# .env file path
ENV_PATH = os.path.join(BASE_DIR, "..", "..", ".env")

# Loading env variables
load_dotenv(ENV_PATH)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", 1))

ALLOWED_HOSTS = ['*']


# Sendgrid config
EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'

ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get('SENDGRID_SERVICE_API_KEY'),
    "SEND_DEFAULTS": {
        "track_clicks": False,
        "track_opens": False,
    },
}

DEFAULT_FROM_EMAIL = os.environ.get('SENDER_EMAIL')  
SERVER_EMAIL = os.environ.get('SENDER_EMAIL')  


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.conf',
    'internal',
    'recruiter',
    'profiles',
    'info',
    'config',
    'bootstrap_datepicker_plus',
    'django_extensions',
    'accounts',
    'anymail',
    'martor'
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

ROOT_URLCONF = 'cdcrc_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'metadata.context_processors.categories_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'cdcrc_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/cdpc/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/cdpc/media/'  # this is the url to access media

FORCE_SCRIPT_NAME = '/cdpc'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

TIME_ZONE = 'Asia/Kolkata'

BOOTSTRAP4 = {
    'include_jquery': True,
}



# Martor Configuration
CSRF_COOKIE_HTTPONLY = False
MARTOR_THEME = 'bootstrap'  # semantic
MARTOR_ENABLE_LABEL = True

MARTOR_UPLOAD_PATH = 'images/uploads/{}'.format(time.strftime("%Y/%m/%d/"))
MARTOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader
MAX_IMAGE_UPLOAD_SIZE = 10485760  # 5MB

MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'true',        # to enable/disable imgur/custom uploader.
    'mention': 'true',      # to enable/disable mention
    'jquery': 'true',       # to include/revoke jquery (require for admin default django)
    'living': 'false',      # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}

MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'image-upload', 'emoji',
    'direct-mention', 'toggle-maximize', 'help'
]


# Google Sheet links and gid
STUDENT_DEMOGRAPHIC_SHEET = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQl9t8FdDcHEpr0RRcTg9xJXm8Z_mCeYvKP9-5HygqkGXOJWk9h67dTecyOunFjKYpdLmd3L0BWWVsN/pub?gid=255931748&single=true&output=tsv'
FACULTY_MEMBERS_SHEET = 'https://docs.google.com/spreadsheets/d/13oeVihTyqm2XTwgJ2sXBX6ghDMoPB7LTffHC7gaWBBE/edit#gid=0'
STUDENT_MEMBERS_SHEET = 'https://docs.google.com/spreadsheets/d/13oeVihTyqm2XTwgJ2sXBX6ghDMoPB7LTffHC7gaWBBE/edit#gid=1884841381'
PLACEMENTS_SHEET = 'https://docs.google.com/spreadsheets/d/13oeVihTyqm2XTwgJ2sXBX6ghDMoPB7LTffHC7gaWBBE/edit#gid=1054840129'
DIRECTORS_SHEET = 'https://docs.google.com/spreadsheets/d/13oeVihTyqm2XTwgJ2sXBX6ghDMoPB7LTffHC7gaWBBE/edit#gid=1913456790'
CHAIRPERSONS_SHEET = 'https://docs.google.com/spreadsheets/d/13oeVihTyqm2XTwgJ2sXBX6ghDMoPB7LTffHC7gaWBBE/edit#gid=1631628272'
VICECHAIRMANS_SHEET = 'https://docs.google.com/spreadsheets/d/13oeVihTyqm2XTwgJ2sXBX6ghDMoPB7LTffHC7gaWBBE/edit#gid=1861857351'
