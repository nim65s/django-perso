# wget https://ksp.fosdem.org/files/keyring.asc.bz2
# bunzip2 -d keyring.asc.bz2
# gpg --import keyring.asc
# rm keyring.asc

from datetime import date

import requests
from pgp_tables.models import KeySigningParty

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importe les clefs du FOSDEM 2015'

    def handle(self, *args, **options):
        ksp, created = KeySigningParty.objects.get_or_create(slug='fosdem15')
        if created:
            ksp.name = 'FOSDEM 2015'
            ksp.detail = '<a href="https://fosdem.org/2015/keysigning/">Free and OpenSource European Developer Meeting 2015</a>, à Bruxelles'
            ksp.date = date(2015, 2, 1)
            ksp.save()
        r = requests.get('https://ksp.fosdem.org/files/keylist.txt')
        r.raise_for_status()
        ksp.add_keys([l.split('/')[1].split()[0] for l in r.content.decode('utf-8').split('\n') if l.startswith('pub')])
