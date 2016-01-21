# wget https://ksp.fosdem.org/2014/files/keyring.asc.bz2
# bunzip2 -d keyring.asc.bz2
# gpg --import keyring.asc
# rm keyring.asc

from datetime import date

from django.core.management.base import BaseCommand

import requests
from pgp_tables.models import KeySigningParty


class Command(BaseCommand):
    help = 'Importe les clefs du FOSDEM 2014'

    def handle(self, *args, **options):
        ksp, created = KeySigningParty.objects.get_or_create(slug='fosdem14')
        if created:
            url = 'https://fosdem.org/2014/keysigning/'
            ksp.name = 'FOSDEM 2014'
            ksp.detail = '<a href="%s">Free and OpenSource European Developer Meeting 2014</a>, à Bruxelles' % url
            ksp.date = date(2014, 2, 2)
            ksp.save()
        r = requests.get('https://ksp.fosdem.org/2014/files/ksp-fosdem2014.txt')
        r.raise_for_status()
        content = r.content.decode('utf-8').split('\n')
        ksp.add_keys([l.split('/')[1].split()[0] for l in content if l.startswith('pub')])
