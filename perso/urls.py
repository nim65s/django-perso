from django.urls import include, path, reverse_lazy
from django.contrib import admin
from django.contrib.sitemaps.views import index, sitemap
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
    path('accounts/profil', profil, name='profil'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('a-propos', TemplateView.as_view(template_name='about.html'), name='about'),

    path('cine/', include('cine.urls')),
    path('comptes/', include('comptes.urls')),
    path('gpg/<str:url>', RedirectView.as_view(url='/PGP/%(url)s', permanent=True)),
    path('PGP/', include('pgp_tables.urls')),
    path('groupe/', include('groupe.urls')),

    path('admin/', admin.site.urls),
    path('photo/', include('perso.urls_photo')),
    path('cgi', permission_denied),
    path('home', RedirectView.as_view(url=reverse_lazy('dmdb:blog'), permanent=True), name="home"),
    path('sitemap\.xml', index, {'sitemaps': sitemaps}),
    path('sitemap-<str:section>\.xml', sitemap, {'sitemaps': sitemaps}),

    path('pebble/', include('pebble.urls')),
    path('fixics/', include('fixics.urls')),
    path('feed', Feed(), name='feed'),
    path('', include('dmdb.urls')),
]
