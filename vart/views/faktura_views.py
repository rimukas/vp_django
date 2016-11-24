from vart.models import Sutartis, Sf
from django.shortcuts import get_object_or_404, render
from django.views import generic
from braces import views
from vart.forms import FakturaUpdateForm, SfForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required


class FakturaAdd(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.CreateView):
    """ Naujos saskaitos fakturos pridejimas prie esancios sutarties.

    """

    # perraso atributa is FormMixin
    form_class = SfForm
    # perraso atributa is FormValidMessageMixin
    form_valid_message = 'Pridėta nauja sąskaita faktūra'
    # perraso atributa is TemplateResponseMixin
    template_name = 'sf_form.html'

    def get(self, request, *args, **kwargs):
        """ Perraso get is klases BaseCreateView.

        Gauna kwargs, perduota id, pagal kuri inicijuojant forma suraso i ja pradines reiksmes

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        id_pk = kwargs['id_pk']
        preke = get_object_or_404(Sutartis, pk=id_pk).kodas.preke
        suma = get_object_or_404(Sutartis, pk=id_pk).suma
        data = get_object_or_404(Sutartis, pk=id_pk).data  # datetime.today().strftime('%Y-%m-%d')

        self.form_class.initial = {
            'pavadinimas': preke,
            'suma': suma,
            'data': data,
            'sutartisid': id_pk
        }
        return super(FakturaAdd, self).get(request, *args, **kwargs)

    # perraso metoda is SingleObjectMixin
    def get_object(self, queryset=None):
        obj = Sutartis.objects.get(pk=self.kwargs['id_pk'])
        return obj

    # perraso metoda is ModelFormMixin
    def get_success_url(self):
        if 'id_pk' in self.kwargs:
            id_pk = self.kwargs['id_pk']
            s = get_object_or_404(Sf, sutartisid_id=id_pk)
            # gaunam vien tik VP koda
            kodas = Sutartis.objects.filter(pk=id_pk).first().kodas.kodas
            self.form_valid_message = self.form_valid_message\
                + ' | data: ' + s.data.strftime('%Y-%m-%d')\
                + ' | S.F. Nr.: ' + s.sf\
                + ' | pirkimo obj.: ' + s.pavadinimas\
                + ' | suma: ' + str(s.suma)
        else:
            kodas = '404'
        return reverse_lazy('sutartis_view', kwargs={'kodas': kodas})

    def get_context_data(self, **kwargs):
        context = super(FakturaAdd, self).get_context_data(**kwargs)
        id_pk = self.kwargs['id_pk']
        context['context'] = get_object_or_404(Sutartis, pk=id_pk)

        # context_view = context['view']
        # context_kwargs = context_view.kwargs['kodas']
        # context['kodas'] = Planas.objects.get(kodas=context_kwargs)
        # context['visi_tiekejai'] = Sutartis.objects.all().values_list('tiekejas', flat=True).distinct()
        return context


class FakturaView(views.LoginRequiredMixin, generic.TemplateView):
    """ Rodo faktura pagal konkrecia sutarti (faktura.html)

    """

    template_name = 'faktura.html'

    # get_context_data() is ContextMixin grazina per URL perduotus parametrus
    def get_context_data(self, **kwargs):
        context = super(FakturaView, self).get_context_data(**kwargs)
        id_pk = self.kwargs['id_pk']
        obj = get_object_or_404(Sutartis, pk=id_pk)
        context['fakturos'] = Sf.objects.filter(sutartisid=obj)
        context['sutartis'] = obj
        return context


class FakturaUpdate(views.LoginRequiredMixin, generic.UpdateView):
    """ Saskaitos fakturos redagavimas

    """
    form_class = FakturaUpdateForm
    form_valid_message = 'Faktūra pataisyta.'
    template_name = 'update_form.html'

    def get_object(self, queryset=None):
        obj = Sf.objects.get(pk=self.kwargs['id_pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(FakturaUpdate, self).get_context_data(**kwargs)
        id_pk = self.kwargs['id_pk']
        sut_id = Sf.objects.get(pk=id_pk).sutartisid_id
        context['formos_pavadinimas'] = 'Sąskaitos faktūros redagavimas'
        context['papildoma_info'] = {
            'Tiekėjas': Sutartis.objects.get(pk=sut_id).tiekejas,
            'Sutarties data': Sutartis.objects.get(pk=sut_id).data,
            'Sutarties suma': Sutartis.objects.get(pk=sut_id).suma}
        return context

    def get_success_url(self):
        if 'id_pk' in self.kwargs:
            id_pk = self.kwargs['id_pk']
        else:
            id_pk = '404'
        return reverse_lazy('faktura', kwargs={'id_pk': id_pk})


@login_required()
def faktura_delete_confirm(request, id_pk):
    context = {
        'context': Sf.objects.get(pk=id_pk)
    }
    return render(request, 'faktura_delete_confirm.html', context)

#
# @login_required()
# def faktura_copy(id_pk):
#     """ Kopijuoja saskaita faktura. Atidaro forma redagavimui is klases FakturaUpdate (update_form.html).
#
#     Kopijavimas padarytas tam, kad maziau duomenu reiketu suvedineti ranka.
#     Nukopijavus tereikia pakeisti besiskiriancius duomenis.
#
#     :param request:
#     :param id_pk:
#     :return:
#     """
#     nauja = Sutartis.objects.get(pk=id_pk)
#     nauja.pk = None
#     nauja.save()
#     return redirect('sutartis_update', id_pk=nauja.pk)


class FakturaDelete(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.DeleteView):

    template_name = 'faktura_delete_confirm.html'
    model = Sf
    form_valid_message = 'Faktūra sėkmingai ištrinta.'

    def get_object(self, queryset=None):
        obj = Sf.objects.get(pk=self.kwargs['id_pk'])
        return obj

    def get_success_url(self):
        if 'id_pk' in self.kwargs:
            id_pk = self.kwargs['id_pk']
            id_pk = Sf.objects.get(pk=id_pk).sutartisid_id
            kodas = Sutartis.objects.get(pk=id_pk).kodas.kodas
        else:
            kodas = '404'
        return reverse_lazy('sutartis_view', kwargs={'kodas': kodas})

