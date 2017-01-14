from django.db import models


class Position(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return '%s: %f, %f' % (self.created, self.lon, self.lat)
