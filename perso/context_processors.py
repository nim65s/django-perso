#-*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string

def google_analytics(request):
    if settings.DEBUG:
        return { 'google_analytics': "" }
    return { 'google_analytics': render_to_string("google_analytics.html", { 'ga_key': settings.GOOGLE_ANALYTICS_KEY}) }
