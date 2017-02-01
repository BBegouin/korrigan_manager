import django
from django.db import models
from django.contrib import admin


# Create your models here.

class Coach(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True,unique=True)
    head = django.db.models.BooleanField(default=False)
    league = models.ForeignKey("League",related_name="league_coachs")
    TD_tot = models.PositiveSmallIntegerField(null=True)
    cas_tot = models.PositiveSmallIntegerField(null=True)
    passes_tot = models.PositiveSmallIntegerField(null=True)
    interception_tot = models.PositiveSmallIntegerField(null=True)
    aggros_tot = models.PositiveSmallIntegerField(null=True)
    nb_win = models.PositiveSmallIntegerField(null=True)
    nb_draw = models.PositiveSmallIntegerField(null=True)
    nb_lose = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.name

    def getPoints(self):
        pass

class League(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True,unique=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    ronde = models.PositiveSmallIntegerField(null=True)
    table = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return "ronde "+self.ronde + " : table " + self.table


class TeamReport(models.Model):
    match = models.ForeignKey("Match",related_name="team_reports")
    Coach = models.ForeignKey("Coach", related_name="report")
    is_winner = models.BooleanField(default=False)
    is_draw = models.BooleanField(default=False)
    is_loser = models.BooleanField(default=False)
    TD = models.PositiveSmallIntegerField(null=True)
    cas = models.PositiveSmallIntegerField(null=True)
    passes = models.PositiveSmallIntegerField(null=True)
    interception = models.PositiveSmallIntegerField(null=True)
    aggros = models.PositiveSmallIntegerField(null=True)

    def getPoints(self):

        #gestion du résultat
        pts_count = 0
        if self.is_winner:
            pts_count += 3000
        elif self.is_draw:
            pts_count += 1000

        #gestion des TD
        pts_count += self.TD * 3

        # sorties
        pts_count += self.cas * 2

        #passes
        pts_count += self.passes * 1

        #interception
        pts_count += self.interception * 2

        #aggros
        pts_count += self.aggros * 2

        return pts_count

class CoachPageAdmin(admin.ModelAdmin):
    fields = (('name', 'league','head'))


admin.site.register(Coach,CoachPageAdmin)
admin.site.register(League)
admin.site.register(Match)
admin.site.register(TeamReport)

