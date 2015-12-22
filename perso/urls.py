from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_confirm, password_reset_done
from django.views.defaults import permission_denied
from django.views.generic import RedirectView

from .views import login_view, logout_view, profil, rsssub_view

admin.autodiscover()

urlpatterns = [

        url(r'^accounts/login', login_view, name='login'),
        url(r'^accounts/logout', logout_view, name='logout'),
        url(r'^accounts/profil', profil, name='profil'),

        url(r'^accounts/password_reset$', password_reset, {'post_reset_redirect': '/accounts/password_reset_done'}, name="password_reset"),
        url(r'^accounts/password_reset_done$', password_reset_done, name='password_reset_done'),
        url(r'^accounts/password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', password_reset_confirm,
            {'post_reset_redirect': '/accounts/password_reset_complete'}, name='password_reset_confirm'),
        url(r'^accounts/password_reset_complete$', password_reset_complete, name='password_reset_complete'),

        url(r'^cine/', include('cine.urls')),
        url(r'^comptes/', include('comptes.urls')),
        url(r'^gpg/(?P<url>.*)$', RedirectView.as_view(url='/PGP/%(url)s', permanent=True)),
        url(r'^PGP/', include('gpg.urls')),
        url(r'^groupe/', include('groupe.urls')),
        url(r'^secret_santa/', include('secret_santa.urls')),
        # url(r'^when/', include('when.urls')),

        url(r'^rss-sub/(?P<url>.+)$', rsssub_view, name='rss-sub'),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^photo/', include('perso.urls_photo')),
        url(r'^cgi', permission_denied),
        url(r'', include('dmdb.urls')),
        ]
