from django.shortcuts import render
from django.http import HttpResponse
from tournament.models import Coach,Match,TeamReport
from django.template import loader
from tournament.core.drawer import draw_round_1,draw_next_round
import xlwt
from django.shortcuts import render, redirect


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

def admin_view_ronde(request,ronde_id):
    # on choppe la liste de match de ronde 1
    match_list = Match.objects.filter(ronde=1)
    context = {
        'match_list': match_list,
    }
    return render(request, 'admin/ronde_1.html', context)

"""
"""
def draw_ronde(request,ronde_id,cancel_ronde):
    ronde_num = int(ronde_id)

    if cancel_ronde:
        cancel_ronde(ronde_num)

    if ronde_num == 1:
        draw_round_1()
    else:
        draw_next_round(ronde_num)
    return redirect('index')

def export_xls_ronde(request,ronde_id):
    ronde_name = "ronde_"+repr(ronde_id)
    filename = '"korrigan_ronde_'+repr(ronde_id)+'.xls"'
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
