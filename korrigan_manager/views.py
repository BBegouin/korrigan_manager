from django.shortcuts import render
from django.http import HttpResponse
from tournament.models import Coach,Match,TeamReport
from django.template import loader

def ronde1(request):
    # on choppe la liste de match de ronde 1
    match_list = Match.objects.filter(ronde=1)
    context = {
        'match_list': match_list,
    }
    return render(request, 'admin/ronde_1.html', context)

def export_ronde(request,ronde_id):
    #si la ronde en question n'est pas tirée, on la tire
    #on choppe les matche de la ronde
    pass
