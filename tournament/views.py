from django.shortcuts import render
from django.http import HttpResponse
from tournament.models import Coach,Match,TeamReport
from django.template import loader


#permet de lister les matchs par ronde
def index(request):
    coach_list = Coach.objects.all().order_by('-points')
    context = {
        'coach_list': coach_list,
    }
    return render(request, 'tournament/index.html', context)

def match(request,match_id):
    resp = "détail du match %s"%match_id
    return HttpResponse(resp)
