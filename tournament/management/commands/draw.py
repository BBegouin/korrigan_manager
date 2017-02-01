__author__ = 'Bertrand'

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
import csv
from tournament.models import League,Coach
import random
from tournament.core.drawer import draw_round_1

data_dir = getattr(settings, "PROJECT_ROOT", None)+'/tournament/datas'

def shuffled_masters_series():
    coaches = Coach.objects.filter(head = True)
    seed = random.randint(1, 10000)
    return coaches.extra(select={'sort_key': 'RAND(%s)' % seed}).order_by('sort_key')




class Command(BaseCommand):
    help = 'draw matchs'

    def handle(self, *args, **options):

        draw_round_1()