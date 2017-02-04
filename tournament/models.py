import django
from django.db import models
from django.contrib import admin
from django.db.models import Sum,Count,Case,When

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
        pass
        # on prend les 4 meilleurs joueurs de la ligue
        # on additionne leurs points, c'est les points de base de la ligue
        # on regarde les performances de la tête de série,
        # pour chaque match, classé par id croissant :
        # est-ce qu'elle a perdu ?
        # si oui on sort
        # si non, est-ce qu'elle a gagné ?
        # si oui on ajoute le bonus victoire

        # on prend tous les matchs victorieux qui ont été joués contre des têtes de série,
        # et pour chaque on ajoute le bonus de kill de tête de série




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
