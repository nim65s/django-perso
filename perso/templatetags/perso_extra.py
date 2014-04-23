# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def url_get(request, key=None, value=None):
    get = request.GET.copy()
    if key:
        get[key] = value
    return "?%s" % get.urlencode()
