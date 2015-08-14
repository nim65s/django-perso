from datetime import datetime

from cine.models import Soiree, get_cinephiles
from comptes.models import Dette, Occasion
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fais les comptes pour les CinéNim'

    def add_arguments(self, parser):
        parser.add_argument('creancier', help='créancier', choices=[u.username for u in get_cinephiles()])
        parser.add_argument('montant', type=float)
        parser.add_argument('description', default='pizza')

    def handle(self, creancier, montant, description, *args, **options):
        occasion, _ = Occasion.objects.get_or_create(nom='CinéNim')

        membres = occasion.membres.all()
        for cinephile in get_cinephiles():
            if cinephile not in membres:
                occasion.membres.add(cinephile)
        occasion.save()

        creancier = User.objects.get(username=creancier)

        soiree = Soiree.objects.last()

        dette = Dette(creancier=creancier, montant=montant, description=description, moment=soiree.datetime(), occasion=occasion)
        dette.save()
        for debiteur in soiree.dispos():
            dette.debiteurs.add(debiteur)
        dette.save()
