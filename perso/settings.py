# -*- coding: utf-8 -*-
"""
Django settings for sourire_interieur project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

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

SECRET_KEY = CONF_DIR.joinpath("secret_key.txt").open().read().strip()

DEBUG = True
INTEGRATION = False
PROD = False

if CONF_DIR.joinpath("integration").is_file():
    DEBUG = False
    INTEGRATION = True
elif CONF_DIR.joinpath("prod").is_file():
    DEBUG = False
    PROD = True

EMAIL_SUBJECT_PREFIX = ("[%s Dev] " if DEBUG or INTEGRATION else "[%s] ") % PROJECT_VERBOSE

EMAIL_USE_SSL = True
EMAIL_HOST = "mail.gandi.net"  # TODO "smtp.%s" % (ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr") ← ça c’est pour ovh…
EMAIL_PORT = 465
EMAIL_HOST_USER = "%s@%s" % (MAIL_USER, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
SERVER_EMAIL = "%s+%s@%s" % (MAIL_USER, PROJECT, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
DEFAULT_FROM_EMAIL = "%s <%s@%s>" % (PROJECT_VERBOSE, MAIL_USER, ALLOWED_HOSTS[0] if SELF_MAIL else "totheweb.fr")
EMAIL_HOST_PASSWORD = CONF_DIR.joinpath("email_password").open().read().strip()

ADMINS = (("Guilhem Saurel", "guilhem+admin-%s@saurel.me" % PROJECT),)
MANAGERS = ADMINS
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_comments',
    'when',
    'cine',
    'comptes',
    'tinymce',
    'sekizai',
    'tagging',
    'mptt',
    'zinnia_bootstrap',
    'zinnia',
    'widget_tweaks',
    'django-ga',
    'django-disqus',
    'bootstrap3',
    'photologue',
    'sortedm2m',
]


MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
]

ROOT_URLCONF = "%s.urls" % PROJECT

WSGI_APPLICATION = "%s.wsgi.application" % PROJECT

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": PROJECT,
        "USER": PROJECT,
        "PASSWORD": CONF_DIR.joinpath("db_password.txt").open().read().strip(),
        "HOST": "localhost",
    }
}

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

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

if not DEBUG:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {"dsn": CONF_DIR.joinpath("raven").open().read().strip()}

if 'zinnia' in INSTALLED_APPS:
    TEMPLATE_LOADERS = (
        "app_namespace.Loader",
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    )

if 'tinymce' in INSTALLED_APPS:
    TINYMCE_DEFAULT_CONFIG = {
        "plugins": "youtube,inlinepopups",
        "theme": "advanced",
        "theme_advanced_buttons1": "bold,italic,underline,|,undo,redo,|,cleanup,|,bullist,numlist,|,link,unlink",
        "theme_advanced_buttons2": "justifyleft,justifycenter,justifyright,justifyfull,|,image,youtube",
        "theme_advanced_buttons3": "",
        "theme_advanced_toolbar_align": "center",
    }

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

if 'django-disqus' in INSTALLED_APPS:
    TEMPLATE_CONTEXT_PROCESSORS.append("django-disqus.context_processors.disqus")
    if PROD:
        DISQUS_SHORTNAME = CONF_DIR.joinpath("disqus").open().read().strip()

if 'django-ga' in INSTALLED_APPS:
    TEMPLATE_CONTEXT_PROCESSORS.append("django-ga.context_processors.google_analytics")
    if PROD:
        GOOGLE_ANALYTICS_KEY = CONF_DIR.joinpath("google_key").open().read().strip()
        GOOGLE_ANALYTICS_SITE = CONF_DIR.joinpath("google_site").open().read().strip()

if 'sekizai' in INSTALLED_APPS:
    TEMPLATE_CONTEXT_PROCESSORS.append("sekizai.context_processors.sekizai")

if 'cine' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES.append("cine.middleware.CheckVoteMiddleware")
