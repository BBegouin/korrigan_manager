__author__ = 'Bertrand'

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
import csv
from tournament.models import League,Coach

data_dir = getattr(settings, "PROJECT_ROOT", None)+'/tournament/datas'

class Command(BaseCommand):
    help = 'load initials datas'

    def handle(self, *args, **options):

        # création des données utilisateur
        admin = User(
             username='Bagouze',
             email='bertrand.begouin@gmail.com',
             password=make_password('bagouze'),
             is_superuser=True,
             is_staff=True
        )
        admin.save()
        Fab = User(
            username='Legalodec',
            email='',
            password=make_password('korrigan'),
            is_superuser=True,
            is_staff=True
        )
        Fab.save()

        # chargement des ligues
        with open(data_dir+'/ligues.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                new_league = League(
                    name = row[0].strip(),
                )
                new_league.save();
                print("ligue "+row[0] + " inserted !")

        # chargement des coachs
        with open(data_dir+'/coachs.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                league_object = League.objects.get(name=row[1])
                is_head = False;
                if row[2] == "1":
                    is_head = True

                new_coach = Coach(
                    name = row[0].strip(),
                    league =league_object,
                    head=is_head
                )
                new_coach.save();
                print("coach " + row[0] + " inserted !")
