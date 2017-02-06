import django
from django.db import models
from django.contrib import admin
from django.db.models import Sum,Count,Case,When
from django.db.models import Q

# Create your models here.

class Coach(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True,unique=True,verbose_name="Nom")
    head = django.db.models.BooleanField(default=False,verbose_name="Tête de série")
    league = models.ForeignKey("League",related_name="coachs",verbose_name="Ligue")
    TD_tot = models.PositiveSmallIntegerField(null=True,verbose_name="TD")
    cas_tot = models.PositiveSmallIntegerField(null=True,verbose_name="cas")
    passes_tot = models.PositiveSmallIntegerField(null=True,verbose_name="Pas")
    interception_tot = models.PositiveSmallIntegerField(null=True,verbose_name="Int")
    aggros_tot = models.PositiveSmallIntegerField(null=True,verbose_name="Aggros")
    nb_win = models.PositiveSmallIntegerField(null=True,verbose_name="Victoire")
    nb_draw = models.PositiveSmallIntegerField(null=True,verbose_name="Nul")
    nb_lose = models.PositiveSmallIntegerField(null=True,verbose_name="Défaites")
    points = models.PositiveSmallIntegerField(null=True,verbose_name="Points")

    class Meta:
        verbose_name = "Classement"
        ordering = ('-points',)

    def update_stats(self):

        #on choppe tous les rapports de match
        myTR = TeamReport.objects.filter(coach = self)

        stats = myTR.aggregate(pts=Sum('points'),
                               TD=Sum('TD'),
                               sor=Sum('sorties'),
                               pas=Sum('passes'),
                               int=Sum('interceptions'),
                               agg=Sum('aggros'),
                               win=Count(Case(When(is_winner=True, then=1))),
                               draw=Count(Case(When(is_draw=True, then=1))),
                               lose=Count(Case(When(is_loser=True, then=1))))

        self.TD_tot = stats['TD']
        self.cas_tot = stats['sor']
        self.passes_tot = stats['pas']
        self.interception_tot = stats['int']
        self.aggros_tot = stats['agg']
        self.nb_win = stats['win']
        self.nb_draw = stats['draw']
        self.nb_lose =stats['lose']
        self.points = stats['pts']

        self.save()

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True,unique=True)
    points = models.PositiveSmallIntegerField(null=True,verbose_name="Points")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ligue"

    # Calcul les points de ligue
    def update_points(self):

        print("update "+self.name)

        #si la ligue n'a pas de tête de série ele ne joue pas pour le challenge inter-ligue
        if Coach.objects.filter(head=True,league=self).count() == 0:
            return

        pts_count = 0
        # on prend les 4 meilleurs joueurs de la ligue
        # on additionne leurs points, c'est les points de base de la ligue
        best4 = Coach.objects.filter(league=self).order_by('-points')[:4].aggregate(pts=Sum('points'))
        pts_count += best4['pts']


        # on regarde les performances de la tête de série,
        head = Coach.objects.get(head=True,league=self)
        # pour chaque match, classé par id croissant :
        head_match_list = Match.objects.filter(team_reports__coach = head).order_by('id')

        head_bonus_point = 0
        for match in head_match_list:
            report = match.team_reports.get(coach=head)
            #au premier match perdu, on sort, le bonus s'arrête
            if report.is_loser:
                break

            if report.is_winner:
                head_bonus_point += 100


        pts_count += head_bonus_point

        # on liste les têtes de séries rencontrées par la ligue :
        # - on prend tous les rapports de match, donc le match parent contient un rapport concernant la ligue
        # - on exclus de cet ensemble les matchs joués par les coachs de la ligue non tête de série,
        # on obtient l'ensemble des rapports de matchs des adversaires,
        # que l'on filtre pour ne garder que les rapports de tête de série
        # que l'on filtre pour ne garder que les rapports perdants

        #on choppe toutes les têtes de séries, hormis celle de la ligue
        heads = Coach.objects.filter(head=True).exclude(league=self)
        #on choppe tous les matchs des têtes de série contre la ligue
        head_matchs = Match.objects.filter(Q(team_reports__coach__id__in=[h.id for h in heads]))\
                        .filter(team_reports__coach__league=self)

        #dans tous ces matchs il faut trouver les matchs gagnés par la ligue
        head_lose_reports = TeamReport.objects.filter(Q(match__id__in=[m.id for m in head_matchs]))\
                            .exclude(coach__league=self)\
                            .filter(is_loser=True)

        # pour chacun de ces rapports, si il exsite un rapport de défaite de la tête de série adverse plus récent,
        # alors les points ne doivent pas être attribués
        kill_head_bonus = 0
        for TR in head_lose_reports:

            first_lose = TeamReport.objects.filter(coach=TR.coach,id__lt=TR.id,is_loser=True).count()

            # si on ne trouve pas de rapport de défaites antérieurs, on attribue les points bonus
            if first_lose is 0:
                kill_head_bonus += 200

        pts_count += kill_head_bonus

        self.points = pts_count
        self.save()





class Match(models.Model):
    ronde = models.PositiveSmallIntegerField(null=True)
    table = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return "ronde "+repr(self.ronde) + " : table " + repr(self.table)

    class Meta:
        verbose_name = "Match"


class TeamReport(models.Model):
    match = models.ForeignKey("Match",related_name="team_reports")
    coach = models.ForeignKey("Coach", related_name="report")
    TD = models.PositiveSmallIntegerField(null=True,blank=True)
    sorties = models.PositiveSmallIntegerField(null=True,blank=True)
    passes = models.PositiveSmallIntegerField(null=True,blank=True)
    interceptions = models.PositiveSmallIntegerField(null=True,blank=True)
    aggros = models.PositiveSmallIntegerField(null=True,blank=True)
    points = models.PositiveSmallIntegerField(null=True,default=0,blank=True)
    is_winner = models.BooleanField(default=False)
    is_draw = models.BooleanField(default=False)
    is_loser = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Rapports de match"

    def __str__(self):
        return self.coach.name

    def update_points(self):

        #mise à jour du statut gagnant / perdant
        foe_report = TeamReport.objects.filter(match = self.match).exclude(id=self.id).first()

        # si le rapport de match de l'adversaire n'est pas setté, on ne fait rien
        if foe_report is not None :
            if foe_report.TD is None:
                foe_report.TD = 0

            if foe_report.TD > self.TD:
                self.is_loser = True;
                self.is_draw = False;
                self.is_winner = False;
            elif foe_report.TD == self.TD:
                self.is_loser = False;
                self.is_draw = True;
                self.is_winner = False;
            elif foe_report.TD < self.TD:
                self.is_loser = False;
                self.is_draw = False;
                self.is_winner = True;

        #gestion du résultat
        pts_count = 0
        if self.is_winner:
            pts_count += 3000
        elif self.is_draw:
            pts_count += 1000

        #gestion des TD
        if self.TD is None:
            self.TD = 0
        pts_count += self.TD * 3

        # sorties
        if self.sorties is None:
            self.sorties = 0
        pts_count += self.sorties * 2

        #passes
        if self.passes is None:
            self.passes = 0
        pts_count += self.passes * 1

        #interception
        if self.interceptions is None:
            self.interceptions = 0
        pts_count += self.interceptions * 2

        #aggros
        if self.aggros is None:
            self.aggros = 0
        pts_count += self.aggros * 5

        self.points = pts_count

        self.save()

        self.coach.update_stats()
