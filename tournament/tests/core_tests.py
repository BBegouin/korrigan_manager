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
        draw_next_round(3)
        draw_next_round(4)

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

    def test_comput_league_points(self):
        """
         Cas de test :
         - vérifier que les bonus de victoire internes sont bien attribués
         - vérifier que les bonus de victoire internes s'arrêtent après la première défaite
         - vérifier que les bonus de victoire externes s'appliquent
         - vérifier que les bonus de victoire externes ne s'applique qu'une seule fois, à la première défaite

        contexte de test :
        - 3 ligues : L1, L2, L3
        - 3 coachs par ligue : L1C1, L1C2, L1C3. Les C1 sont têtes de série

        matchs
        L1C1 - L2C2 : 1-0 => +100
        L1C2 - L3C1 : 1-0 => +200

        """
        L1 = League(name="L1")
        L1.save()

        L2 = League(name="L2")
        L2.save()

        L3 = League(name="L3")
        L3.save()

        L1C1 = Coach(league=L1,head=True,name="L1C1")
        L1C1.save()
        L1C2 = Coach(league=L1,head=False,name="L1C2")
        L1C2.save()

        L2C1 = Coach(league=L2,head=True,name="L2C1")
        L2C1.save()
        L2C2 = Coach(league=L2,head=False,name="L2C2")
        L2C2.save()

        L3C1 = Coach(league=L3,head=True,name="L3C1")
        L3C1.save()
        L3C2 = Coach(league=L3,head=False,name="L3C2")
        L3C2.save()

        match_L1C1_L2C2 = Match(ronde=1,table=1)
        match_L1C1_L2C2.save()

        TR_L1C1_1 = TeamReport(coach = L1C1,
                               match = match_L1C1_L2C2,
                               TD=1,
                               sorties=0,
                               passes=0,
                               interceptions=0,
                               aggros=0)
        TR_L1C1_1.save()
        TR_L2C2_1 = TeamReport(coach = L2C2,
                               match = match_L1C1_L2C2,
                               TD=0,
                               sorties=0,
                               passes=0,
                               interceptions=0,
                               aggros=0)
        TR_L2C2_1.save()

        match_L2C1_L1C2 = Match(ronde=1,table=2)
        match_L2C1_L1C2.save()

        TR_L1C2_2 = TeamReport(coach = L1C2,
                               match = match_L2C1_L1C2,
                               TD=1,
                               sorties=0,
                               passes=0,
                               interceptions=0,
                               aggros=0)
        TR_L1C2_2.save()
        TR_L2C1_2 = TeamReport(coach = L2C1,
                               match = match_L2C1_L1C2,
                               TD=0,
                               sorties=0,
                               passes=0,
                               interceptions=0,
                               aggros=0)
        TR_L2C1_2.save()

        # mise à jour des points des TR
        TR_L1C1_1.update_points()
        TR_L2C2_1.update_points()
        TR_L1C2_2.update_points()
        TR_L2C1_2.update_points()

        # mise à jour des points coachs
        L1C1.update_stats()
        L1C2.update_stats()
        L2C1.update_stats()
        L2C2.update_stats()

        # mise à jour les ligues
        L1.update_points()
        L2.update_points()

        #la ligue 1 devrait avoir :
        # - 6006 points de victoires
        # - 100 points bonus tête
        # - 200 points bonus kill tête
        self.assertEqual(L1.points,6306)

        #la ligue 2 devrait avoir :
        # - 0 points de victoires
        # - 0 pts bonus tête
        # - 0 pts bonus kill tête
        self.assertEqual(L2.points,0)

        #
        # Deuxième ronde
        # la tête de série de ligue 1 va perdre contre l'ancienne tête de série 2
        #

        match_L1C1_L2C1 = Match(ronde=2,table=1)
        match_L1C1_L2C1.save()

        TR_L1C1_3 = TeamReport(coach = L1C1,
                               match = match_L1C1_L2C1,
                               TD=0,
                               sorties=0,
                               passes=0,
                               interceptions=0,
                               aggros=0)
        TR_L1C1_3.save()
        TR_L2C1_3 = TeamReport(coach = L2C1,
                               match = match_L1C1_L2C1,
                               TD=1,
                               sorties=0,
                               passes=0,
                               interceptions=0,
                               aggros=0)
        TR_L2C1_3.save()

        # mise à jour des points des TR
        TR_L1C1_3.update_points()
        TR_L2C1_3.update_points()

        # mise à jour des points coachs
        L1C1.update_stats()
        L2C1.update_stats()

        # mise à jour les ligues
        L1.update_points()
        L2.update_points()

            #la ligue 1 devrait avoir :
        # - 6006 points de victoires
        # - 100 points bonus tête
        # - 200 points bonus kill tête
        self.assertEqual(L1.points,6306)

        #la ligue 2 devrait avoir :
        # - 3003 points de victoires
        # - 0 pts bonus tête
        # - 200 pts bonus kill tête
        self.assertEqual(L2.points,3203)




