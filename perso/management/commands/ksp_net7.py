import requests
from bs4 import BeautifulSoup
from pgp_tables.models import KeySigningParty

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importe les clefs de net7'

    def handle(self, *args, **options):
        ksp, created = KeySigningParty.objects.get_or_create(slug='net7')
        if created:
            ksp.name = 'Net7'
            ksp.detail = 'Clefs des membres de <a href="https://www.bde.enseeiht.fr/clubs/net7/">net7</a> & <a href="http://www.bde.inp-toulouse.fr/clubs/inp-net/contact.php">INP-net</a>'
            ksp.save()
        r = requests.get('http://www.bde.inp-toulouse.fr/clubs/inp-net/contact.php')
        r.raise_for_status()
        ksp.add_keys([k['id'] for k in BeautifulSoup(r.content).find_all('span', {'class': 'OpenPGP-Key'})])
