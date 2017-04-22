from django.conf.urls import url

from .views import fixics

app_name = 'fixics'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+).ics', fixics, name="fixics"),
]
