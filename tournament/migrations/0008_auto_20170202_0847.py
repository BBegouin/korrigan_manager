# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 08:47
from __future__ import unicode_literals

from django.db import migrations
from django.db import migrations
from tournament.models import League,Coach
from django.contrib.auth.hashers import make_password
from django.conf import settings
import csv

def create_admin_user(apps, schema_editor):
     User = apps.get_registered_model('auth', 'User')
     admin = User(
         username='Bagouze',
         email='bertrand.begouin@gmail.com',
         password=make_password('bagouze'),
         is_superuser=True,
         is_staff=True
     )
     admin.save()

data_dir = getattr(settings, "PROJECT_ROOT", None)+'/tournament/datas'

def load_datas(apps, schema_editor):

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

    print("====================================================")
    print("==== Fin de l'insertion des données de base ========")
    print("====================================================")


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_auto_20170202_0845'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
        migrations.RunPython(load_datas),
    ]
