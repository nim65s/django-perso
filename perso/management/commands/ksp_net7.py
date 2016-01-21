from django.core.management.base import BaseCommand

import requests
from bs4 import BeautifulSoup
from pgp_tables.models import KeySigningParty


class Command(BaseCommand):
    help = 'Importe les clefs de net7'

    def handle(self, *args, **options):
        ksp, created = KeySigningParty.objects.get_or_create(slug='net7')
        if created:
            ksp.name = 'Net7'
            ksp.detail = 'Clefs des membres de <a href="%s">net7</a> & <a href="%s">INP-net</a>' % (
                'http://www.bde.enseeiht.fr/clubs/net7/',
                'http://www.bde.inp-toulouse.fr/clubs/inp-net/contact.php')
            ksp.save()
        r = requests.get('http://www.bde.inp-toulouse.fr/clubs/inp-net/contact.php')
        r.raise_for_status()
        ksp.add_keys([k['id'] for k in BeautifulSoup(r.content).find_all('span', {'class': 'OpenPGP-Key'})])
