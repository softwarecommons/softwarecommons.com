import os
from pathlib import Path

import django_aspen

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = os.environ.get('DEBUG', 'no') == 'yes'

if 'SECRET_KEY' in os.environ:
	SECRET_KEY = os.environ['SECRET_KEY']

if 'FLY_APP_NAME' in os.environ:
    ENFORCE_HOST = 'new.softwarecommons.com'
    ALLOWED_HOSTS = [ENFORCE_HOST, f'{os.environ["FLY_APP_NAME"]}.fly.dev']
    CSRF_TRUSTED_ORIGINS = [f'https://{ENFORCE_HOST}']
else:
    ENFORCE_HOST = 'localhost:8000'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

if 'SENTRY_DSN' in os.environ:
	import sentry_sdk
	sentry_sdk.init(
		dsn=os.environ['SENTRY_DSN'],
		enable_tracing=True,
	)

ASPEN_REQUEST_PROCESSOR = django_aspen.install(project_root=BASE_DIR, www_root=BASE_DIR / 'www')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'enforce_host.EnforceHostMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

import dj_database_url

DATABASES = dict(default=dj_database_url.config())


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = 'static/'
WHITENOISE_INDEX_FILE = True
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
