from django.conf.urls import patterns, include, url
from django.contrib import admin

from perso.views import login_view, logout_view, about

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', 'when.views.home'),  # TODO: another home ?

        url(r'^about$', about, name='about'),
        url(r'^login$', login_view, name='login'),
        url(r'^logout$', logout_view, name='logout'),

        url(r'^when/', include('when.urls', namespace="when")),

        url(r'^admin/', include(admin.site.urls)),
)
