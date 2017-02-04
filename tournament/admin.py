from django.contrib import admin
from tournament.models import Coach,League,Match,TeamReport
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

class CoachPageAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'points',
                    'league',
                    'nb_win',
                    'nb_draw',
                    'nb_lose',
                    'TD_tot',
                    'cas_tot',
                    'passes_tot',
                    'interception_tot',
                    'aggros_tot',
                    'head']

    list_filter = ('head', 'league','nb_win')

class LeaguePageAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'points',]

class MatchPageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class TeamReportPageAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ['coach',
                    'match',
                    'TD',
                    'sorties',
                    'passes',
                    'interceptions',
                    'aggros',
                    'points']

    list_editable = ('TD','sorties','passes','interceptions','aggros')
    list_filter = ('match__ronde',)
    search_fields = ['coach__name','match__ronde']
    list_per_page = 10

    # fonction appelée à chaque sauvegarde d'objet TeamReport
    def save_model(self, request, obj, form, change):
        #on choppe le rapport de match de l'adversaire, si il a été rempli on mets à jour les points
        foe_tr = obj.match.team_reports.exclude(coach=obj.coach).first()
        if foe_tr.TD is not None:
            obj.update_points()
            foe_tr.update_points()
        obj.save()


class MyAdminSite(AdminSite):
    site_header = "coincoin"

    def get_urls(self):
        """Add our dashboard view to the admin urlconf. Deleted the default index."""
        from django.conf.urls import url

        urls = super(MyAdminSite, self).get_urls()
        del urls[0]
        custom_url = [url(r'^$',  self.admin_view(self.index), name='index')]

        return custom_url + urls

    @never_cache
    def index(self, request, extra_context=None):

        matchs = TeamReport.objects.all()
        ronde_1_drawn = TeamReport.objects.filter(match__ronde=1).count() > 0

        #la ronde est finie si tout les rapports de matchs sont remplis
        ronde_is_finished = TeamReport.objects.filter(TD__isnull=True).count() == 0

        #la ronde est commencé si le nombre de rapport non remplis est inférieur au nombre de coach
        ronde_not_started = TeamReport.objects.filter(TD__isnull=True).count() == Coach.objects.all().count()
        ronde_2_drawn = TeamReport.objects.filter(match__ronde=2).count() > 0
        ronde_3_drawn = TeamReport.objects.filter(match__ronde=3).count() > 0
        ronde_4_drawn = TeamReport.objects.filter(match__ronde=4).count() > 0
        ronde_5_drawn = TeamReport.objects.filter(match__ronde=5).count() > 0
        context = {
            'match_list': matchs,
            'ronde_1_drawn':ronde_1_drawn,
            'ronde_2_drawn':ronde_2_drawn,
            'ronde_3_drawn':ronde_3_drawn,
            'ronde_4_drawn':ronde_4_drawn,
            'ronde_5_drawn':ronde_5_drawn,
            'ronde_finished':ronde_is_finished,
            'ronde_not_started':ronde_not_started
        }
        return super().index(request, extra_context=context)

admin.site = MyAdminSite()
admin.autodiscover()

# Register your models here.
admin.site.register(Coach,CoachPageAdmin)
admin.site.register(League,LeaguePageAdmin)
admin.site.register(Match,MatchPageAdmin)
admin.site.register(TeamReport,TeamReportPageAdmin)
admin.site.site_header = 'Korrigan Manager - Administration'

