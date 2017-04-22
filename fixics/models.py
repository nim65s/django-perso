from django.db import models
from django.urls import reverse


class RedirectICS(models.Model):
    slug = models.SlugField(unique=True)
    url = models.URLField()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('fixics:fixics', kwargs={'slug': self.slug})
