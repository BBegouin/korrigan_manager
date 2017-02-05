from django.contrib import admin
from tournament.models import Coach,League,Match,TeamReport
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from tournament.admin import CoachPageAdmin,MatchPageAdmin,LeaguePageAdmin,TeamReportPageAdmin



