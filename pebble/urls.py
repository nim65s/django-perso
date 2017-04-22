from django.conf.urls import url

from .views import pebble

app_name = 'pebble'

urlpatterns = [
    url(r'^(?P<lat>[0-9.]+)/(?P<lon>[0-9.]+)', pebble, name="pebble"),
    url(r'^', pebble),
]
