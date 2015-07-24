# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User

from cine.models import Soiree, get_cinephiles
from comptes.models import Occasion

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fais les comptes pour les CinéNim'

    def add_arguments(self, parser):
        parser.add_argument('creancier', help='créancier', choices=[u.username for u in get_cinephiles()])
        parser.add_argument('montant', type=float)
        parser.add_argument('description', default='pizza')

    def handle(self, *args, creancier, montant, description, **options):
        occasion, _ = Occasion.objects.get_or_create(nom='CinéNim')

        membres = occasion.membres.all()
        for cinephile in get_cinephiles():
            if cinephile not in membres:
                occasion.membres.add(cinephile)
        occasion.save()

        creancier = User.objects.get(username=creancier)
        debiteurs = Soiree.objects.last().dispos()

        Dette(creancier=creancier, montant=montant, debiteurs=debiteurs, description=description, moment=datetime.now(), occasion=occasion).save()
