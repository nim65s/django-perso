from datetime import date

from django.core.management.base import BaseCommand

from pgp_tables.models import KeySigningParty


class Command(BaseCommand):
    help = 'Importe les clefs du Capitole du Libre 2016'

    def handle(self, *args, **options):
        url = 'https://2016.capitoledulibre.org/programme.html#key-signing-party'
        keys = ['6B17EA1E', 'C3F54A72', '68290509', 'D2475B28', 'FA1051C4', '83D97FFC', '17D7E01C', 'C9D718A1',
                '292FF6C3', 'F94E9DF5', 'E4583762', 'D4BC9401', '0642FA40', '37D128F8', '264C4323', '80A5ECE3',
                'D64CE766', '8D18CA37', '4653CF28', 'F8F5F173', 'F3B2CEDE', '56C4754A', '45C81AF8', '9D0EECA7',
                'A64B5107', '7011B752', 'DCF76136', 'B10D7ED4', '54AC263D', '175B313D', '7D422C30', 'D9E7AABF',
                '63F5CF3A', 'C068E338', '78758817', '5CD09700']
        ksp, created = KeySigningParty.objects.get_or_create(slug='CdL16')
        if created:
            ksp.name = 'Capitole du Libre 2016'
            ksp.detail = '<a href="%s">Capitôle du Libre 2016</a>, à Toulouse' % url
            ksp.date = date(2016, 11, 20)
            ksp.save()
        ksp.add_keys(keys)
