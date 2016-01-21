from datetime import date

from django.core.management.base import BaseCommand

from pgp_tables.models import KeySigningParty


class Command(BaseCommand):
    help = 'Importe les clefs du Capitole du Libre 2014'

    def handle(self, *args, **options):
        url = 'http://2014.capitoledulibre.org/programme/presentation/49/'
        keys = ['089047FE', '382A5C4D', '4653CF28', '552CF98B', '5F4445B5', '682A3916', '6B17EA1E', '72F93B05',
                '78758817', 'C2AA477E', 'DD999172', 'F3B2CEDE']
        ksp, created = KeySigningParty.objects.get_or_create(slug='CdL14')
        if created:
            ksp.name = 'Capitole du Libre 2014'
            ksp.detail = '<a href="%s">Capitôle du Libre 2014</a>, à Toulouse' % url
            ksp.date = date(2014, 11, 16)
            ksp.save()
        ksp.add_keys(keys)
