from vart.models import Planas, Sutartis, Sf
from django.views import generic
from braces import views
from django.core.urlresolvers import reverse_lazy
from datetime import date, datetime
from vart.forms import SutartisUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required()
def sutartis_view(request, kodas):
    """ Rodo visu sutarciu langa pagal konkretu VP koda (sutartis.html).

    :param request:
    :param kodas:
    :return:
    """
    data_cookie = request.COOKIES.get('date_to')
    if data_cookie is None:
        data_iki = date.today()
    else:
        data_iki = datetime.strptime(data_cookie, '%Y-%m-%d')

    data_cookie = request.COOKIES.get('date_from')
    if data_cookie is None:
        data_nuo = date(date.today().year, 1, 1)
    else:
        data_nuo = datetime.strptime(data_cookie, '%Y-%m-%d')

    kodas = get_object_or_404(Planas, kodas=kodas)

    kodas_filtered = Sutartis.objects.filter(
        data__range=[data_nuo, data_iki]).filter(
         kodas_id=kodas)

    context = {
        'data_nuo': data_nuo.strftime('%Y-%m-%d'),
        'data_iki': data_iki.strftime('%Y-%m-%d'),
        'kodas': kodas,
        'kodas_filtered': kodas_filtered,
        'fakturos': Sf.objects.all()
    }

    return render(request, 'sutartis.html', context)


class SutartisUpdate(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.UpdateView):
    """ Atidaro forma sutarties redagavimui (update_form.html).

    """

    def get_object(self, queryset=None):
        obj = Sutartis.objects.get(pk=self.kwargs['id_pk'])
        return obj

    form_class = SutartisUpdateForm
    form_valid_message = 'Sutartis pataisyta!'
    template_name = 'update_form.html'

    def form_valid(self, form):
        """ Atlikus POST suvienodina imones pavadinimo uzrasyma. Pvz., "IMONESPAVADINIMAS, UAB"

        :param form:
        :return:
        """
        tipas = ['IĮ', 'AB', 'UAB', 'TŪB', 'KŪB', 'VĮ', 'VAĮ']
        appnd = ''
        imone = form.cleaned_data['tiekejas']
        imone_list = imone.replace('\'', '"').replace(',', '').upper().split(' ')
        for li in imone_list:
            if li in tipas:
                appnd = ', ' + imone_list.pop(imone_list.index(li))

        form.instance.tiekejas = ' '.join(imone_list) + appnd

        return super(SutartisUpdate, self).form_valid(form)

    def get_success_url(self):
        if 'id_pk' in self.kwargs:
            id_pk = self.kwargs['id_pk']
            kodas = Sutartis.objects.get(pk=id_pk).kodas_id
        else:
            kodas = '404'
        return reverse_lazy('sutartis_view', kwargs={'kodas': kodas})

    def get_context_data(self, **kwargs):
        context = super(SutartisUpdate, self).get_context_data(**kwargs)
        id_pk = self.kwargs['id_pk']
        context['formos_pavadinimas'] = 'Sandorio sutarties redagavimas'
        # cia gali buti zodynas is bet kiek ir bet kokiu kombinaciju {raktas_1:reiksme_1, raktas_n:reiksme_n,...}
        context['papildoma_info'] = {'VP Kodas': Sutartis.objects.get(pk=id_pk).kodas}
        return context


@login_required()
def sutartis_copy(request, id_pk):
    """ Kopijuoja sutarti. Atidaro forma redagavimui is klases SutartisUpdate (update_form.html).

    Kopijavimas padarytas tam, kad maziau duomenu reiketu suvedineti ranka.
    Nukopijavus tereikia pakeisti besiskiriancius duomenis.

    :param request:
    :param id_pk:
    :return:
    """

    nauja = Sutartis.objects.get(pk=id_pk)
    nauja.pk = None
    nauja.save()
    return redirect('sutartis_update', id_pk=nauja.pk)


@login_required()
def sutartis_delete_confirm(request, id_pk):
    context = {
        'id_pk': Sutartis.objects.get(pk=id_pk).id,
        'kodas': Sutartis.objects.get(pk=id_pk),
        'debug': 'DEBUG'
    }
    return render(request, 'sutartis_delete_confirm.html', context)


class SutartisDelete(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.DeleteView):

    template_name = 'sutartis_delete_confirm.html'
    model = Sutartis
    form_valid_message = 'Sutartis sėkmingai ištrinta.'

    def get_object(self, queryset=None):
        obj = Sutartis.objects.get(pk=self.kwargs['id_pk'])
        return obj

    def get_success_url(self):
        if 'id_pk' in self.kwargs:
            id_pk = self.kwargs['id_pk']
            kodas = Sutartis.objects.get(pk=id_pk).kodas_id
        else:
            kodas = '404'
        return reverse_lazy('sutartis_view', kwargs={'kodas': kodas})


class SutartisAdd(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.CreateView):

    form_class = SutartisUpdateForm
    form_valid_message = 'Pridėta nauja sutartis '
    template_name = 'sutartis_form.html'

    def form_valid(self, form):
        """ Atlikus POST, suvienodina imones pavadinimo uzrasyma. Pvz., "IMONESPAVADINIMAS, UAB"

        :param form:
        :return:
        """
        tipas = ['IĮ', 'AB', 'UAB', 'TŪB', 'KŪB', 'VĮ', 'VAĮ']
        appnd = ''
        imone = form.cleaned_data['tiekejas']
        imone_list = imone.replace('\'', '"').replace(',', '').upper().split(' ')
        for li in imone_list:
            if li in tipas:
                appnd = ', ' + imone_list.pop(imone_list.index(li))

        # data = form.cleaned_data['data']
        # form.instance.data = data
        form.instance.tiekejas = ' '.join(imone_list) + appnd
        # I forma automatiskai irasom VP koda. Ji gaunam kaip objekta, nes tai ManyToOne ForeignKey laukas
        form.instance.kodas = Planas.objects.get(kodas=self.kwargs['kodas'])
        return super(SutartisAdd, self).form_valid(form)

    def get_success_url(self):
        if 'kodas' in self.kwargs:
            kodas = self.kwargs['kodas']
            s = Sutartis.objects.filter(kodas=kodas).last()
            self.form_valid_message = self.form_valid_message \
                + ' | data: ' + s.data.strftime('%Y-%m-%d') \
                + ' | tiekėjas: ' + s.tiekejas \
                + ' | suma: ' + str(s.suma)
        else:
            kodas = '404'
        return reverse_lazy('sutartis_view', kwargs={'kodas': kodas})

    def get_context_data(self, **kwargs):
        context = super(SutartisAdd, self).get_context_data(**kwargs)
        context_view = context['view']
        context_kwargs = context_view.kwargs['kodas']
        context['kodas'] = Planas.objects.get(kodas=context_kwargs)
        context['visi_tiekejai'] = Sutartis.objects.all().values_list('tiekejas', flat=True).distinct()
        return context
