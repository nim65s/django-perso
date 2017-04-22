from django.test import TestCase

from .models import RedirectICS

SLUG = 'toulibre'
URL = 'http://www.agendadulibre.org/ical.php?tag=toulibre'


class FixICSTest(TestCase):
    def test(self):
        instance = RedirectICS.objects.create(slug=SLUG, url=URL)
        self.assertEqual(str(instance), SLUG)
        self.assertEqual(self.client.get(instance.get_absolute_url()).status_code, 301)
