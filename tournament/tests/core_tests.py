__author__ = 'Bertrand'
from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from tournament.models import Coach,League,TeamReport,Match
from tournament.core.drawer import draw_round_1,draw_next_round,cancel_ronde
from django.db.models import Count
from django.db.models import Q
import random

class CoreTest(TestCase):

    """
        On teste le tirage au sort de la première rone
    """
    def test_draw_round_1(self):

        # on tire la ronde 1
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


    """
     On teste le tirage au sort de la seconde ronde
    """
    def test_draw_round_2(self):

        draw_round_1()

        #on va remplir les teamreports de données aléatoires
        for TR in TeamReport.objects.all():
            TR.TD = random.randint(0, 5)
            TR.sorties = random.randint(0, 5)
            TR.passes = random.randint(0, 5)
            TR.interceptions = random.randint(0, 5)
            TR.aggros = random.randint(0, 5)
            TR.save()

        for TR in TeamReport.objects.all():
            TR.update_points()
            TR.coach.update_stats()

        all_coaches = Coach.objects.all().order_by('-points')
        for c in all_coaches:
            print(c.name+" : "+repr(c.points)+" pts")

        draw_next_round(2)

        #on vérifie que chaque coach ne joue qu'une seule fois à la ronde 2
        # ==> On doit donc avoir le même nombre de rapport de match que de coachs
        self.assertEqual(TeamReport.objects.filter(match__ronde=2).count(),Coach.objects.all().count(),)

    """
     On teste l'annulation de la ronde 1
    """
    def test_cancel_ronde_1(self):

        """
         Test d'annulation de la ronde 1
        """
        # on vide la BDD
        Match.objects.all().delete()

        # on tire la ronde 1
        draw_round_1()

        #on annule la ronde
        cancel_ronde(1)

        # on vérifie qu'on a plus de match en base et plus de rapport de match en base
        self.assertEqual(Match.objects.all().count(),0)
        self.assertEqual(TeamReport.objects.all().count(),0)


    """
     On teste l'annulation de la ronde 2
    """
    def test_cancel_ronde_2(self):

        draw_round_1()

        #on va remplir les teamreports de données aléatoires
        for TR in TeamReport.objects.all():
            TR.TD = random.randint(0, 5)
            TR.sorties = random.randint(0, 5)
            TR.passes = random.randint(0, 5)
            TR.interceptions = random.randint(0, 5)
            TR.aggros = random.randint(0, 5)
            TR.save()

        for TR in TeamReport.objects.all():
            TR.update_points()
            TR.coach.update_stats()

        all_coaches = Coach.objects.all().order_by('-points')
        for c in all_coaches:
            print(c.name+" : "+repr(c.points)+" pts")

        draw_next_round(2)

        cancel_ronde(2)

        #on vérifie que nous n'avons plus de match de ronde 2, mais que les matchs de ronde 1 sont encore là
        self.assertEqual(TeamReport.objects.filter(match__ronde=2).count(),0)
        self.assertEqual(Match.objects.filter(ronde=2).count(),0)
        self.assertEqual(TeamReport.objects.filter(match__ronde=1).count(),Coach.objects.all().count())
        self.assertEqual(Match.objects.filter(ronde=1).count(),Coach.objects.all().count()/2)




