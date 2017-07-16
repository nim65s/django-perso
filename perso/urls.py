from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import index, sitemap
from django.core.urlresolvers import reverse_lazy
from django.views.defaults import permission_denied
from django.views.generic import RedirectView, TemplateView

from dmdb.sitemaps import BlogEntrySitemap
from photologue.sitemaps import GallerySitemap, PhotoSitemap

from .feeds import Feed
from .views import profil

sitemaps = {
    'blog': BlogEntrySitemap,
    'gallery': GallerySitemap,
    'photo': PhotoSitemap,
}

urlpatterns = [
    url(r'^accounts/profil', profil, name='profil'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^a-propos$', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r'^cine/', include('cine.urls')),
    url(r'^comptes/', include('comptes.urls')),
    url(r'^gpg/(?P<url>.*)$', RedirectView.as_view(url='/PGP/%(url)s', permanent=True)),
    url(r'^PGP/', include('pgp_tables.urls')),
    url(r'^groupe/', include('groupe.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^photo/', include('perso.urls_photo')),
    url(r'^cgi', permission_denied),
    url(r'^home$', RedirectView.as_view(url=reverse_lazy('dmdb:blog'), permanent=True), name="home"),
    url(r'^sitemap\.xml$', index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}),

    url(r'^pebble/', include('pebble.urls')),
    url(r'^fixics/', include('fixics.urls')),
    url(r'^feed', Feed(), name='feed'),
    url(r'', include('dmdb.urls')),
]
