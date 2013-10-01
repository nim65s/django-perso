from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import TemplateView
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from perso.views import login_view, logout_view, profil

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
        url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
        url(r'^about$', TemplateView.as_view(template_name='about.html'), name="about"),

        url(r'^accounts/login', login_view, name='login'),
        url(r'^accounts/logout', logout_view, name='logout'),
        url(r'^accounts/profil', profil, name='profil'),

        url(r'^accounts/password_reset$', password_reset, {'post_reset_redirect' : '/accounts/password_reset_done'}, name="password_reset"),
        url(r'^accounts/password_reset_done$', password_reset_done, name='password_reset_done'),
        url(r'^accounts/password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', password_reset_confirm,
            {'post_reset_redirect' : '/accounts/password_reset_complete'}, name='password_reset_confirm'),
        url(r'^accounts/password_reset_complete$', password_reset_complete, name='password_reset_complete'),

        #url(r'^blog/', include('blog.urls', namespace="blog")),
        url(r'^cine/', include('cine.urls', namespace="cine")),
        url(r'^comptes/', include('comptes.urls', namespace="comptes")),
        url(r'^when/', include('when.urls', namespace="when")),

        url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
        url(r'^admin/', include(admin.site.urls)),
        #url(r'^tinymce/', include('tinymce.urls')),
)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
