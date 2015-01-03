from braces.views import SuperuserRequiredMixin
from photologue.models import Gallery

from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
        url(r'^albums/$', ListView.as_view(queryset=Gallery.objects.is_public()), name='gallery-list'),
        url(r'^album/(?P<slug>[\-\d\w]+)/$', DetailView.as_view(model=Gallery), name='pl-gallery'),
        url(r'^photo/(?P<slug>[\-\d\w]+)/$', PhotoDetailView.as_view(), name='pl-photo'),
        )
