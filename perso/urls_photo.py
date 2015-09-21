from photologue.models import Gallery

from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from .views import GalleryPhotoDetailView, PhotoDetailView

urlpatterns = patterns('',
        url(r'^albums/$', ListView.as_view(template_name='photologue/gallery_list.html', queryset=Gallery.objects.is_public), name='gallery-list'),
        url(r'^album/(?P<slug>[\-\d\w]+)/(?P<index>\d+)$', GalleryPhotoDetailView.as_view(), name='pl-gallery-photo'),
        url(r'^album/(?P<slug>[\-\d\w]+)/$', DetailView.as_view(model=Gallery), name='pl-gallery'),
        url(r'^photo/(?P<slug>[\-\d\w]+)/$', PhotoDetailView.as_view(), name='pl-photo'),
        )
