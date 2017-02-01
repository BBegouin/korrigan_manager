from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from tournament.models import Coach,League,TeamReport,Match
from tournament.core.drawer import draw_round_1
from django.db.models import Count
from django.db.models import Q

class TestDraw(TestCase):

    def test_draw_round_1(self):
        draw_round_1()

        # on vérifie que tous les coachs ont bien un match et un seul :
        # ==> On vérifie que toutes les têtes de séries ont bien un match :
        self.assertEqual(TeamReport.objects.filter(coach__head=True).count(),Coach.objects.filter(head=True).count(),)

        # ==> Il faut vérifier qu'il n'ya aucun doublon dans les coachs affectés à un team report
        coach_doublon = TeamReport.objects.values('coach__name').annotate(Count('id')) .order_by().filter(id__count__gt=1)
        self.assertEqual(coach_doublon.count(),0)

        # ==> On doit donc avoir le même nombre de rapport de match que de coachs
        self.assertEqual(TeamReport.objects.all().count(),Coach.objects.all().count(),)

        # on vérifie que les têtes de série sont contre des joueurs appartenant à des ligues différentes
        head_foes = Coach.objects.filter(Q(report__match__team_reports__coach__id__in=[c.id for c in Coach.objects.filter(head=True)])).exclude(head=True)
        ligue_doublon_count = head_foes.values('league__name').annotate(Count('id')).order_by().filter(id__count__gt=1).count()
        self.assertEqual(ligue_doublon_count,0)

        # on vérifie que chaque tête de série à bien un adversaire non tête de série
        self.assertEqual(head_foes.count(),Coach.objects.filter(head=True).count())


