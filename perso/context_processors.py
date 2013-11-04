#-*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string


def google_analytics(request):
    if settings.DEBUG:
        return {'google_analytics': ""}
    return {'google_analytics': render_to_string("google_analytics.html", {'ga_key': settings.GOOGLE_ANALYTICS_KEY, 'ga_site': settings.GOOGLE_ANALYTICS_SITE})}


def disqus(request):
    if settings.DEBUG:
        return {'disqus': ""}
    return {'disqus': render_to_string("disqus.html", {'disqus_shortname': settings.DISQUS_SHORTNAME})}
