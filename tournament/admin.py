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
        coach_list = Coach.objects.all().order_by('-points')
        context = {
            'coach_list': coach_list,
        }
        return super().index(request, extra_context=context)

admin.site = MyAdminSite()
admin.autodiscover()

# Register your models here.
#admin.site.index_template = "admin/index.html"
admin.site.register(Coach,CoachPageAdmin)
admin.site.register(League,LeaguePageAdmin)
admin.site.register(Match,MatchPageAdmin)
admin.site.register(TeamReport,TeamReportPageAdmin)
admin.site.site_header = 'Korrigan Manager - Administration'

