from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf.urls.i18n import i18_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from perso.views import *

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = i18_patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^blog', include('cms.urls')),
)

urlpatterns = patterns('',
        url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
        url(r'^about$', TemplateView.as_view(template_name='about.html'), name="about"),

        url(r'^accounts/login', login_view, name='login'),
        url(r'^accounts/logout', logout_view, name='logout'),
        url(r'^accounts/profil', profil, name='profil'),

        url(r'^when/', include('when.urls', namespace="when")),
        url(r'^cine/', include('cine.urls', namespace="cine")),
        url(r'^comptes/', include('comptes.urls', namespace="comptes")),

        url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
) + urlpatterns


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
