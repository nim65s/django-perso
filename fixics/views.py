from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from .models import RedirectICS


def fixics(request, slug):
    obj = get_object_or_404(RedirectICS, slug=slug)
    return HttpResponsePermanentRedirect(obj.url)
