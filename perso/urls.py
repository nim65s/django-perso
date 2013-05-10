from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from perso.views import *

admin.autodiscover()


urlpatterns = patterns('',
        url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
        url(r'^about$', TemplateView.as_view(template_name='about.html'), name="about"),

        url(r'^accounts/login', login_view, name='login'),
        url(r'^accounts/logout', logout_view, name='logout'),
        url(r'^accounts/profil', profil, name='profil'),

        url(r'^weblog/', include('weblog.urls', namespace="weblog")),
        url(r'^when/', include('when.urls', namespace="when")),
        url(r'^cine/', include('cine.urls', namespace="cine")),
        url(r'^comptes/', include('comptes.urls', namespace="comptes")),

        url(r'^admin/', include(admin.site.urls)),
)
