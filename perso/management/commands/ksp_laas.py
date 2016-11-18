from datetime import date

from django.core.management.base import BaseCommand

from pgp_tables.models import KeySigningParty


class Command(BaseCommand):
    help = 'Importe les clefs du LAAS'

    def handle(self, *args, **options):
        url = 'https://www.laas.fr/public/'
        keys = ['4653CF28', '4D76D5C7', '83D97FFC', '37D128F8', 'D9E7AABF', '700865F7', '7D422C30', '175B313D',
                '148DC13D', 'D64CE766', '56C4754A', 'EE7D48D8', 'F89E32B1', '530D5B9B']
        ksp, created = KeySigningParty.objects.get_or_create(slug='laas')
        if created:
            ksp.name = 'LAAS'
            ksp.detail = 'Clefs des membres du <a href="%s">LAAS</a>' % url
            ksp.date = date(2016, 11, 17)
            ksp.save()
        ksp.add_keys(keys)
