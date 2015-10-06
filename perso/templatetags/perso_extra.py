from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def url_get(request, key=None, value=None):
    get = request.GET.copy()
    if key:
        get[key] = value
    return "?%s" % get.urlencode()


@register.filter
def email(email, request):
    at, dot = ('<span class="%s"></span>' % i for i in ['at', 'dot'])
    return mark_safe('<span class="mail">%s</span>' % (email if request.user.is_authenticated() else email.replace('@', at).replace('.', dot)))
