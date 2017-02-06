__author__ = 'Bertrand'

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
import csv
from tournament.models import League,Coach
import random
from tournament.core.drawer import draw_round_1
from tournament.models import TeamReport

data_dir = getattr(settings, "PROJECT_ROOT", None)+'/tournament/datas'

class Command(BaseCommand):
    help = 'permet de complèter automatiquement une ronde à des fins de test : syntaxe "python manage.py complete_ronde 1"'

    def add_arguments(self, parser):
        parser.add_argument('ronde', nargs='+', type=int)

    def handle(self, *args, **options):

        ronde_to_complete = options['ronde'];
        tr =TeamReport.objects.filter(match__ronde=ronde_to_complete[0])

        #on remplit tous les rapports de match
        for TR in tr:
            TR.TD = random.randint(0, 5)
            TR.sorties = random.randint(0, 5)
            TR.passes = random.randint(0, 5)
            TR.interceptions = random.randint(0, 5)
            TR.aggros = random.randint(0, 5)
            TR.save()

        for TR in TeamReport.objects.all():
            TR.update_points()
            TR.coach.update_stats()
            TR.coach.league.update_points()