"""
Django settings for perso project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from os.path import abspath, dirname, join
from pathlib import Path

PROJECT = "perso"
PROJECT_VERBOSE = "Nim’s web.log \o/"
MAIL_USER = "majo"
SELF_MAIL = True
ALLOWED_HOSTS = ["saurel.me"]
ALLOWED_HOSTS.append("www.%s" % ALLOWED_HOSTS[0])

BASE_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = Path("/etc/django/") / PROJECT

if not CONF_DIR.is_dir():
    CONF_DIR.mkdir(parents=True)

SECRET_KEY = (CONF_DIR / "secret_key.txt").open().read().strip()

DEBUG, INTEGRATION, PROD = False, False, False

if (CONF_DIR / "integration").is_file():
    INTEGRATION = True
elif (CONF_DIR / "prod").is_file():
    PROD = True
else:
    DEBUG = True

EMAIL_SUBJECT_PREFIX = ("[%s Dev] " if DEBUG or INTEGRATION else "[%s] ") % PROJECT_VERBOSE

EMAIL_USE_SSL = True
EMAIL_HOST = "mail.gandi.net"
EMAIL_PORT = 465
EMAIL_HOST_USER = "%s@%s" % (MAIL_USER, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
SERVER_EMAIL = "%s+%s@%s" % (MAIL_USER, PROJECT, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
DEFAULT_FROM_EMAIL = "%s <%s@%s>" % (PROJECT_VERBOSE, MAIL_USER, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
EMAIL_HOST_PASSWORD = (CONF_DIR / "email_password").open().read().strip()

ADMINS = (("Guilhem Saurel", "guilhem+admin-%s@saurel.me" % PROJECT),)
MANAGERS = ADMINS

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'cine',
    'comptes',
    'bootstrap3',
    'photologue',
    'sortedm2m',
    'pgp_tables',
    'groupe',
    'dmdb',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '%s.urls' % PROJECT

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PROJECT,
        'USER': PROJECT,
        'PASSWORD': (CONF_DIR / 'db_password.txt').open().read().strip(),
        'HOST': 'localhost',
    }
}

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

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

MEDIA_ROOT = join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static_dest') if DEBUG else '/var/www/%s/static_dest' % PROJECT

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

if (Path(BASE_DIR) / PROJECT / 'context_processors.py').is_file():
    TEMPLATES[0]['OPTIONS']['context_processors'].append('%s.context_processors.%s' % (PROJECT, PROJECT))

if not DEBUG:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {"dsn": (CONF_DIR / "raven").open().read().strip()}

if 'bootstrap3' in INSTALLED_APPS:
    BOOTSTRAP3 = {
        "horizontal_label_class": "col-md-3",
        "horizontal_field_class": "col-md-6",
    }
    if DEBUG:
        BOOTSTRAP3["jquery_url"] = "/static/js/jquery.min.js"
        BOOTSTRAP3["base_url"] = "/static/"
    else:
        BOOTSTRAP3["jquery_url"] = "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"

if 'cine' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES.append('cine.middleware.CheckVoteMiddleware')

if 'photologue' in INSTALLED_APPS:
    PHOTOLOGUE_GALLERY_SAMPLE_SIZE = 10
