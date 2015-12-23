from django.conf.urls import include, url
from django.contrib import admin
from django.views.defaults import permission_denied
from django.views.generic import RedirectView

from .views import profil

admin.autodiscover()

urlpatterns = [
        url(r'^accounts/profil', profil, name='profil'),
        url(r'^accounts/', include('django.contrib.auth.urls')),

        url(r'^cine/', include('cine.urls')),
        url(r'^comptes/', include('comptes.urls')),
        url(r'^gpg/(?P<url>.*)$', RedirectView.as_view(url='/PGP/%(url)s', permanent=True)),
        url(r'^PGP/', include('gpg.urls')),
        url(r'^groupe/', include('groupe.urls')),

        url(r'^admin/', include(admin.site.urls)),
        url(r'^photo/', include('perso.urls_photo')),
        url(r'^cgi', permission_denied),
        url(r'', include('dmdb.urls')),
        ]
