import os
from os.path import dirname, isfile, join

BASE_DIR = dirname(dirname(__file__))

ADMINS = (('Guilhem Saurel', 'guilhem+admin-perso@saurel.me'),)
MANAGERS = ADMINS

DEBUG = True
if isfile('/etc/nim/perso/prod'):
    DEBUG = False
    EMAIL_SUBJECT_PREFIX = '[Perso] '
    with open('/etc/nim/perso/google_key') as f:
        GOOGLE_ANALYTICS_KEY = f.read().strip()
    with open('/etc/nim/perso/google_site') as f:
        GOOGLE_ANALYTICS_SITE = f.read().strip()
    with open('/etc/nim/perso/disqus') as f:
        DISQUS_SHORTNAME = f.read().strip()
else:
    EMAIL_SUBJECT_PREFIX = '[Perso-Dev] '

# TODO 1.7
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'ssl0.ovh.net'
# EMAIL_PORT = 465
EMAIL_HOST = 'smtp.totheweb.fr'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'majo@totheweb.fr'
SERVER_EMAIL = 'majo+perso@totheweb.fr'
DEFAULT_FROM_EMAIL = 'Perso <majo@totheweb.fr>'
with open('/etc/nim/majo_pw') as f:
    EMAIL_HOST_PASSWORD = f.read().strip()


TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['saurel.me', 'www.saurel.me', 'perso.saurel.me']

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'p0c9pc$)q4(9-1(qht(rw1)i5t8*le+xd$mgtrx*pqfcrvge#@'
else:
    with open('/etc/nim/perso/secret_key.txt') as f:
        SECRET_KEY = f.read().strip()

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'when',
    'cine',
    'comptes',
    'tinymce',
    'dajaxice',
    'dajax',
    'sekizai',
    'zinnia_bootstrap',
    'zinnia',
    'tagging',
    'mptt',
    'django.contrib.comments',  # :@
    'widget_tweaks',
    'perso',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    "perso.context_processors.google_analytics",
    "perso.context_processors.disqus",
)


ROOT_URLCONF = 'perso.urls'

WSGI_APPLICATION = 'perso.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

with open('/etc/nim/perso/db_password.txt') as f:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'perso',
            'USER': 'persopguser',
            'PASSWORD': f.read().strip(),
            'HOST': 'localhost',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (join(BASE_DIR, "static"),)
MEDIA_ROOT = join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

if DEBUG:
    STATIC_ROOT = join(BASE_DIR, "static_dest")
else:
    STATIC_ROOT = '/var/www/perso/static-dest'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)

TEMPLATE_DIRS = (join(BASE_DIR, 'templates'),)

TEMPLATE_LOADERS = (
    'app_namespace.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'youtube,inlinepopups',
    'theme': 'advanced',
    'theme_advanced_buttons1': 'bold,italic,underline,|,undo,redo,|,cleanup,|,bullist,numlist,|,link,unlink',
    'theme_advanced_buttons2': 'justifyleft,justifycenter,justifyright,justifyfull,|,image,youtube',
    'theme_advanced_buttons3': '',
    'theme_advanced_toolbar_align': 'center',

}

BOOTSTRAP3 = {}
if DEBUG:
    BOOTSTRAP3['jquery_url'] = "/static/js/jquery.min.js"
    BOOTSTRAP3['base_url'] = "/static/"
else:
    BOOTSTRAP3['jquery_url'] = "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"


with open('/etc/nim/perso/raven') as f:
    RAVEN_CONFIG = {'dsn': f.read().strip()}
