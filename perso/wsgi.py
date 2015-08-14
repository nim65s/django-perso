"""
WSGI config for perso project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from locale import LC_ALL, setlocale

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perso.settings")

setlocale(LC_ALL, 'fr_FR.UTF-8')

application = get_wsgi_application()
