from django.shortcuts import render
from django.http import HttpResponse
from tournament.models import Coach,Match,TeamReport,League
from django.template import loader
from tournament.core.drawer import draw_round_1,draw_next_round,cancel_ronde
import xlwt
from django.shortcuts import render, redirect

#
# Affiche la page d'accueil du front
#
def index(request):
    coach_list = Coach.objects.all().order_by('-points')
    context = {
        'coach_list': coach_list,
    }
    return render(request, 'tournament/index.html', context)

#
# Affiche les pages de ronde du front
#
def view_ronde(request,ronde_id):
    #on selectionne tous les matchs de la ronde
    match_list = Match.objects.filter(ronde=int(ronde_id))
    context = {
        'match_list': match_list,
        'ronde_id':ronde_id
    }
    return render(request, 'tournament/ronde.html', context)

def match(request,match_id):
    resp = "détail du match %s"%match_id
    return HttpResponse(resp)

def admin_view_ronde(request,ronde_id):
    # on choppe la liste de match de ronde
    match_list = Match.objects.filter(ronde=int(ronde_id))
    context = {
        'match_list': match_list,
        'ronde_id':ronde_id
    }
    return render(request, 'admin/ronde.html', context)

"""
"""
def draw_ronde(request,ronde_id,cancel_ronde_id):
    ronde_num = int(ronde_id)

    if cancel_ronde_id:
        cancel_ronde(cancel_ronde_id)

    if ronde_num == 1:
        draw_round_1()
    else:
        draw_next_round(ronde_num)

    return HttpResponse()

"""
 Export le classement général sous format excel
"""
def export_xls_ranking(request):
    filename = 'korrigan_8_classement_général.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('classement_général')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Place','Coach','Ligue','points','V','N','D','TD','Sorties','Passes','Interceptions','agressions']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Coach.objects.all().values_list('name','league__name','points','nb_win','nb_draw','nb_lose','TD_tot','cas_tot','passes_tot','interception_tot','aggros_tot')
    for row in rows:
        row_num += 1

        for col_num in range(len(row)+1):
            if col_num == 0:
                ws.write(row_num, col_num, row_num, font_style)
                continue
            ws.write(row_num, col_num, row[col_num-1], font_style)

    wb.save(response)
    return response

#
# export le classement par ligues
#
def export_xls_league_ranking(request):
    filename = 'korrigan_8_classement_des_ligues.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('classement_ligues')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Place','Ligue','points']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = League.objects.all().values_list('name','points').order_by('-points')
    for row in rows:
        row_num += 1

        for col_num in range(len(row)+1):
            if col_num == 0:
                ws.write(row_num, col_num, row_num, font_style)
                continue
            ws.write(row_num, col_num, row[col_num-1], font_style)

    wb.save(response)
    return response

def export_xls_ronde(request,ronde_id):
    ronde_name = "ronde_"+repr(ronde_id)
    filename = 'korrigan_ronde_'+repr(ronde_id)+'.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ronde_name')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Table', 'Coach 1', 'Coach 2']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Match.objects.filter(ronde=ronde_id).values_list('table')
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row[0], font_style)
        ws.write(row_num, 1, TeamReport.objects.filter(match__ronde=ronde_id,match__table=row[0]).first().coach.name, font_style)
        ws.write(row_num, 2, TeamReport.objects.filter(match__ronde=ronde_id,match__table=row[0]).last().coach.name, font_style)

    wb.save(response)
    return response
