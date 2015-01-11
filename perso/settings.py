# -*- coding: utf-8 -*-
"""
Django settings for sourire_interieur project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import dirname, join

from pathlib import Path

PROJECT = "perso"
PROJECT_VERBOSE = u"Nim’s web.log \o/"
MAIL_USER = "majo"
SELF_MAIL = True
ALLOWED_HOSTS = ["saurel.me"]
ALLOWED_HOSTS.append("www.%s" % ALLOWED_HOSTS[0])

BASE_DIR = dirname(dirname(__file__))
CONF_DIR = Path("/etc/nim/" + PROJECT)

if not CONF_DIR.is_dir():
    CONF_DIR.mkdir(parents=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONF_DIR.joinpath("secret_key.txt").open().read().strip()

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True
INTEGRATION = False

if CONF_DIR.joinpath("integration").is_file():
    DEBUG = False
    INTEGRATION = True
elif CONF_DIR.joinpath("prod").is_file():
    DEBUG = False
    GOOGLE_ANALYTICS_KEY = CONF_DIR.joinpath("google_key").open().read().strip()
    GOOGLE_ANALYTICS_SITE = CONF_DIR.joinpath("google_site").open().read().strip()
    DISQUS_SHORTNAME = CONF_DIR.joinpath("disqus").open().read().strip()

EMAIL_SUBJECT_PREFIX = ("[%s Dev] " if DEBUG or INTEGRATION else "[%s] ") % PROJECT_VERBOSE

# TODO 1.7
# EMAIL_USE_SSL = True
# EMAIL_HOST = "ssl0.ovh.net"
# EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_HOST = "mail.gandi.net"  # "smtp.%s" % (ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr") ← ça c’est pour ovh…
EMAIL_PORT = 587
EMAIL_HOST_USER = "%s@%s" % (MAIL_USER, ALLOWED_HOSTS[0])
SERVER_EMAIL = "%s+%s@%s" % (MAIL_USER, PROJECT, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
DEFAULT_FROM_EMAIL = "%s <%s@%s>" % (PROJECT_VERBOSE, MAIL_USER, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
EMAIL_HOST_PASSWORD = CONF_DIR.joinpath("email_password").open().read().strip()

ADMINS = (("Guilhem Saurel", "guilhem+admin-%s@saurel.me" % PROJECT),)
MANAGERS = ADMINS
TEMPLATE_DEBUG = DEBUG

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_comments',
    'when',
    'cine',
    'comptes',
    'tinymce',
    'sekizai',
    'tagging',
    'mptt',
    PROJECT,
    'zinnia_bootstrap',
    'zinnia',
    'widget_tweaks',
    'django-ga',
    'django-disqus',
    'raven.contrib.django.raven_compat',
    'bootstrap3',
    'photologue',
    'sortedm2m',
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cine.middleware.CheckVoteMiddleware",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "sekizai.context_processors.sekizai",
    "django-ga.context_processors.google_analytics",
    "django-disqus.context_processors.disqus",
)

ROOT_URLCONF = "%s.urls" % PROJECT

WSGI_APPLICATION = "%s.wsgi.application" % PROJECT


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": PROJECT,
        "USER": PROJECT,
        "PASSWORD": CONF_DIR.joinpath("db_password.txt").open().read().strip(),
        "HOST": "localhost",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (join(BASE_DIR, "static"),)
MEDIA_ROOT = join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = join(BASE_DIR, "static_dest") if DEBUG else "/var/www/%s/static_dest" % PROJECT

CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "127.0.0.1:11211",
            }
        }


TEMPLATE_DIRS = (join(BASE_DIR, "templates"),)

TEMPLATE_LOADERS = (
    "app_namespace.Loader",
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

RAVEN_CONFIG = {"dsn": CONF_DIR.joinpath("raven").open().read().strip()}

TINYMCE_DEFAULT_CONFIG = {
    "plugins": "youtube,inlinepopups",
    "theme": "advanced",
    "theme_advanced_buttons1": "bold,italic,underline,|,undo,redo,|,cleanup,|,bullist,numlist,|,link,unlink",
    "theme_advanced_buttons2": "justifyleft,justifycenter,justifyright,justifyfull,|,image,youtube",
    "theme_advanced_buttons3": "",
    "theme_advanced_toolbar_align": "center",
}

BOOTSTRAP3 = {}
if DEBUG:
    BOOTSTRAP3["jquery_url"] = "/static/js/jquery.min.js"
    BOOTSTRAP3["base_url"] = "/static/"
else:
    BOOTSTRAP3["jquery_url"] = "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"

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
