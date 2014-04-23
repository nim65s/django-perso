from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from zinnia.sitemaps import CategorySitemap, EntrySitemap, TagSitemap

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_confirm, password_reset_done
from django.views.generic import TemplateView

from .views import login_view, logout_view, profil, rsssub_view

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',

        url(r'^accounts/login', login_view, name='login'),
        url(r'^accounts/logout', logout_view, name='logout'),
        url(r'^accounts/profil', profil, name='profil'),

        url(r'^accounts/password_reset$', password_reset, {'post_reset_redirect': '/accounts/password_reset_done'}, name="password_reset"),
        url(r'^accounts/password_reset_done$', password_reset_done, name='password_reset_done'),
        url(r'^accounts/password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', password_reset_confirm,
            {'post_reset_redirect': '/accounts/password_reset_complete'}, name='password_reset_confirm'),
        url(r'^accounts/password_reset_complete$', password_reset_complete, name='password_reset_complete'),

        url(r'^cine/', include('cine.urls', namespace="cine")),
        url(r'^comptes/', include('comptes.urls', namespace="comptes")),
        url(r'^when/', include('when.urls', namespace="when")),

        url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^tinymce/', include('tinymce.urls')),
        url(r'^rss-sub/(?P<url>.+)$', rsssub_view, name='rss-sub'),
        url(r'', include('zinnia.urls')),
        url(r'^cgi', 'django.views.defaults.permission_denied'),
)


if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns

sitemaps = {'tags': TagSitemap, 'blog': EntrySitemap, 'categories': CategorySitemap}

urlpatterns += patterns('django.contrib.sitemaps.views',
    url(r'^sitemap.xml$', 'index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
