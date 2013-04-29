from django.conf.urls import patterns, include, url
from django.contrib import admin

from perso.views import *

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', home, name='home'),

        url(r'^about$', about, name='about'),

        url(r'^accounts/login', login_view, name='login'),
        url(r'^accounts/logout', logout_view, name='logout'),
        url(r'^accounts/profil', profil, name='profil'),

        url(r'^when/', include('when.urls', namespace="when")),
        url(r'^cine/', include('cine.urls', namespace="cine")),

        url(r'^admin/', include(admin.site.urls)),
)
