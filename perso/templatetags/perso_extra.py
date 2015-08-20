from django import template

register = template.Library()


@register.simple_tag
def url_get(request, key=None, value=None):
    get = request.GET.copy()
    if key:
        get[key] = value
    return "?%s" % get.urlencode()

@register.filter
def path_in_url(request, path):
    return path in request.path
