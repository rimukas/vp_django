# from django.shortcuts import render

from templated_docs import fill_template
from templated_docs.http import FileResponse

from django.contrib.auth.models import User
from django.db.models import Sum, Count, Max
from vart.models import Planas, Sutartis
from datetime import date


def print_users(request):
    doctype = 'pdf'

    context = {'user': User.objects.all()}
    filename = fill_template('reports/rep.odt', context, output_format=doctype)
    visible_filename = 'vartotojai.{}'.format(doctype)

    return FileResponse(filename, visible_filename)


def print_planas(request):
    doctype = 'pdf'
    context = {'context': Planas.objects.filter(organizatorius=request.user.username)}
    filename = fill_template('reports/planas.odt', context, output_format=doctype)
    visible_filename = 'planas.{}'.format(doctype)

    return FileResponse(filename, visible_filename)


def print_ivykdymas(request):
    doctype = 'pdf'

    metai = date.today().year
    sutartys = Sutartis.objects.filter(data__year=metai)

    # dar prafiltruojam sutartis pagal prisijungusio vartotojo VP kodus (visus),
    # kad neimtu kitu vartotoju ivestu sutarciu
    user_name = request.user.username
    planas = Planas.objects.filter(organizatorius=user_name)
    sut_id = sutartys.filter(kodas__in=planas)

    # velniskai sudetinga uzklausa ):
    # is jos paimtus duomenis atvaizduoja pagrindiniam puslapyje "ivykdytu pirkimu apzvalgoje".
    # paimam pagal data ir prisijungusio vartotojo VP kodus isfiltruotas sutartis sut_id,
    # grupuojam jas pagal laukus:
    # Sutartys.kodas->Planas.preke,
    # Sutartys.kodas->Planas.kodas,
    # Sutartys.kodas->Planas.islaidos,
    # toliau pagal atbulini ForeignKey is Sutartys i Sf skaiciuojam
    # Sf.sf count, Sf.suma sum, ir dar suskaiciuojam procentus.
    # gaunam QuerySet, priskiriam prie "fakturos", ir siunciam i puslapi.
    fakturos = sut_id.values(
        'kodas__preke', 'kodas__kodas', 'kodas__islaidos'). \
        annotate(
        sf_count=Count('sf__sf'),
        sf_sum=Sum('sf__suma'),
        proc=(Sum('sf__suma') / Max('kodas__islaidos')) * 100)

    context = {
        'fakturos': fakturos,
        'username': User.objects.get(username=user_name),
        'laikotarpis': str(metai),
    }

    filename = fill_template('reports/ivykdymas.odt', context, output_format=doctype)
    visible_filename = 'ivykdymas.{}'.format(doctype)

    return FileResponse(filename, visible_filename)

