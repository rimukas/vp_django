from vart.models import Planas
from django.views import generic
from braces import views
from django.core.urlresolvers import reverse_lazy
from model_utils.models import SoftDeletableModel
from vart.forms import PlanasAddForm, PlanasUpdateForm, LaikotarpisForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect


@login_required()
def laikotarpis(request):
    """ Filtruojamo laikotarpio nustatymui ir VP kodui pasirinkti.

    Parodo langa pries sutarties pildyma (zurnalo_laikotarpis.html).
    Jame galima nusistatyti filtruojama laikotarpi ir butina pasirinkti
    VP koda, kuriuo bus pildoma sutartis.

    :param request:
    :return:
    """
    data_cookie = request.COOKIES.get('date_to')
    if data_cookie is None:
        data_iki = date(date.today().year, date.today().month, date.today().day)
    else:
        data_iki = datetime.strptime(data_cookie, '%Y-%m-%d')

    data_cookie = request.COOKIES.get('date_from')
    if data_cookie is None:
        data_nuo = date(date.today().year, 1, 1)
    else:
        data_nuo = datetime.strptime(data_cookie, '%Y-%m-%d')

    current_user = request.user.username
    kodas = Planas.objects.filter(organizatorius=current_user)

    if request.method == 'POST':
        forma = LaikotarpisForm(request.POST)
        if forma.is_valid():
            date_from = forma.cleaned_data['date_from']
            date_to = forma.cleaned_data['date_to']
            kodas = forma.cleaned_data['kodas']
            response = redirect('sutartis_view', kodas=kodas)
            # expiration = datetime.strptime(datetime.today(), "%Y-%m-%d")
            expiration = datetime.today() + timedelta(hours=8)
            response.set_cookie(key='date_from', value=date_from, expires=expiration)
            response.set_cookie(key='date_to', value=date_to, expires=expiration)
            return response

    else:
        forma = LaikotarpisForm()
    return render(request, 'zurnalo_laikotarpis.html', {
        'form': forma,
        'kodas': kodas,
        'nuo_kada': data_nuo,
        'iki_kada': data_iki
    })


class PlanasView(views.LoginRequiredMixin, generic.TemplateView):
    """ Prisijungusio vartotojo planas (planas.html).
    """
    template_name = 'planas.html'

    def get_context_data(self, **kwargs):
        context = super(PlanasView, self).get_context_data(**kwargs)
        current_user = self.request.user.username
        context['current_user'] = current_user
        context['kodas'] = Planas.objects.filter(organizatorius_id=current_user).values()
        return context


class PlanasAdd(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.CreateView):
    """ Naujo VP kodo pridejimo forma (planas_create.html).

    """
    form_class = PlanasAddForm
    form_valid_message = 'Įvestas naujas kodas: '
    template_name = 'planas_create.html'
    success_url = reverse_lazy('planas_add')

    def form_valid(self, form):
        form.instance.organizatorius = self.request.user
        self.form_valid_message += \
            form.cleaned_data['kodas'] + ', ' \
            + form.cleaned_data['preke'] + '. '\
            + 'Gali įvesti dar vieną kodą arba spausk viršutinį meniu mygtuką "Planas".'
        return super(PlanasAdd, self).form_valid(form)


class PlanasUpdate(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.UpdateView):
    """ VP kodo redagavimo forma (planas_create.html).

    """

    form_class = PlanasUpdateForm
    form_valid_message = 'Planas pataisytas!'
    template_name = 'planas_create.html'
    success_url = reverse_lazy('planas')

    def get_object(self, queryset=None):
        obj = Planas.objects.get(kodas=self.kwargs['kodas'])
        return obj


class PlanasDelete(
        views.LoginRequiredMixin,
        generic.edit.DeleteView,
        SoftDeletableModel):

        # form_class = PlanasDeleteForm
        # form_valid_message = 'Planas pataisytas!'
        # template_name = 'planas_delete_confirm.html'
        model = Planas
        form_valid_message = 'Planas sėkmingai ištrintas.'

        # success_url = reverse_lazy('planas')

        def get_object(self, queryset=None):
            obj = Planas.objects.get(kodas=self.kwargs['kodas'])
            return obj

        def get_success_url(self):
            return reverse_lazy('planas')


@login_required()
def planas_delete_confirm(request, kodas):
    """ Patvirtinimo langas VP kodo istrynimui.

    Is tiesu VP kodo neistrina, o tik priskiria ji vartotojui "delete",
    tad reikalui esant ji vel galima atstatyti ar priskirti kitam vartotojui

    :param request:
    :param kodas:
    :return:
    """
    kodas = Planas.objects.get(kodas=kodas)
    return render(request, 'planas_delete_confirm.html', {'kodas': kodas})