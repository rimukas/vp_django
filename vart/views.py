from django.http import HttpResponseRedirect
from .forms import PlanasAddForm, RegistrationForm, PlanasUpdateForm, LoginForm, SutartisUpdateForm, LaikotarpisForm, PlanasDeleteForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from braces import views
from .models import Planas, Sutartis
from datetime import date, datetime, timedelta
import re
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic.edit import CreateView


class HomePageView(generic.TemplateView):
    """ Pagrindinis (home) puslapis.

    TODO:
    Jame turetu buti rodoma atskira informacija prisijungusiems ir
    neprisijungusiems vartotojams.

    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        user_name = self.request.user.username
        context['kodai'] = Planas.objects.filter(organizatorius=user_name)
        return context


class SignUpView(
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.CreateView):
    """ Registracija. Šiaip turi būti nenaudojama
    (naujus vartotojus priregistruoti ir suteikti jiems teises turi administratorius per admin panel)

    """
    form_valid_message = 'Tu sekmingai prisiregistravai!'
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'


class LoginView(
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.FormView):
    """ Prisijungimas prie svetaines.

    Vartotojai privalo tureti administratoriaus suteiktus prisijungimo duomenis.

    """

    form_valid_message = 'Tu prisiloginai!'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(
        views.LoginRequiredMixin,
        views.MessageMixin,
        generic.RedirectView):
    """ Atsijungimas nuo svetaines.

    """
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("Tu atsijungei. Norint peržiūrėti ar suvesti duomenis turi vėl prisijungti.")
        return super(LogOutView, self).get(request, *args, **kwargs)


# @login_required()
# def planas_view(request):
#     """ Rodo prisiregistravusio vartotojo plana (planas.html).
#
#     :param request:
#     :return:
#     """
#     # current_user = request.user.get_full_name()
#     current_user = request.user.username
#     context = {
#         'current_user': current_user,
#         'kodas': Planas.objects.filter(
#             organizatorius_id=current_user).values()}
#     return render(request, 'planas.html', context)


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


# @login_required()
# def kodas_view(request, kodas_nr):
#     context = {
#         'kodas_nr': kodas_nr
#     }
#     return render(request, 'kodas_view.html', context)


class PlanasAdd(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.CreateView):
    """ Naujo VP kodo pridejimo forma (planas_create.html).

    """
    form_class = PlanasAddForm
    form_valid_message = 'Nauja plano eilutė įvesta sėkmingai!'
    template_name = 'planas_create.html'
    success_url = reverse_lazy('planas_add')

    def form_valid(self, form):
        form.instance.organizatorius = self.request.user
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


@login_required()
def planas_delete(request, kodas):
    """ Plano (vieno VP kodo) pasalinimas.

    Is tiesu VP kodo neistrina, o tik priskiria ji vartotojui "delete",
    tad reikalui esant ji vel galima atstatyti ar priskirti kitam vartotojui

    :param request:
    :param kodas:
    :return:
    """
    # naujas Plano objektas su kodu, perduotu per nuoroda
    k = Planas.objects.get(kodas=kodas)
    # naujas User objektas, kurio vardas "delete"
    u = User.objects.get(username='deleted')
    # "delete" vartotojui priskiriam perduota koda
    k.organizatorius = u
    # saugo duombazeje
    k.save()
    # permetam i puslapi "planas.html"
    current_user = request.user.username
    context = {
        'current_user': current_user,
        'kodas': Planas.objects.filter(
            organizatorius_id=current_user).values()}
    return render(request, 'planas.html', context)


# uzkomentuotas Planas eilutes pasalinimas is duombazes
'''
def planas_delete_confirm(request, kodas):
    context = {"kodas": Planas.objects.get(kodas=kodas)}
    # return render(request, 'kodas_view.html', context)
    return render(request, 'planas_delete_form.html', context)
'''
'''
class PlanasDelete(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.DeleteView):
    # form_class = PlanasDeleteForm
    # form_valid_message = 'Planas pataisytas!'
    template_name = 'planas_delete_form.html'
    model = Planas
    form_valid_message = 'Kodas sėkmingai ištrintas.'

    success_url = reverse_lazy('planas')

    def get_object(self, queryset=None):
        obj = Planas.objects.get(kodas=self.kwargs['kodas'])
        return obj
'''
# -----------------------------


@login_required()
def sutartis_view(request, kodas):
    """ Rodo visu sutarciu langa pagal konkretu VP koda (sutartis.html).

    :param request:
    :param kodas:
    :return:
    """
    kodas_p = kodas
    data_cookie = request.COOKIES.get('date_to')
    if data_cookie is None:
        data_iki = date(date.today())
    else:
        data_iki = datetime.strptime(data_cookie, '%Y-%m-%d')

    data_cookie = request.COOKIES.get('date_from')
    if data_cookie is None:
        data_nuo = date(date.today().year, 1, 1)
    else:
        data_nuo = datetime.strptime(data_cookie, '%Y-%m-%d')

    # current_user = request.user.get_full_name()
    # current_user = user
    # kodas = Planas.objects.filter(organizatorius=current_user)
    # kodai = Planas.objects.filter(organizatorius=user).kodas
    kodas = get_object_or_404(Planas, kodas=kodas)

    kodas_filtered = Sutartis.objects.filter(
        data__range=[data_nuo, data_iki]).filter(
         kodas_id=kodas)

    context = {
        # 'planas_kodas': Planas.objects.get(kodas=kodas),
        # 'kodai': Planas.objects.filter(organizatorius=user),
        # 'current_user': user,
        'data_nuo': data_nuo.strftime('%Y-%m-%d'),
        'data_iki': data_iki.strftime('%Y-%m-%d'),
        'kodas': kodas,
        'kodas_filtered': kodas_filtered
    }

    return render(request, 'sutartis.html', context)


class SutartisUpdate(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.UpdateView):
    """ Atidaro forma sutarties redagavimui (sutartis_form.html).

    """

    def get_object(self, queryset=None):
        obj = Sutartis.objects.get(pk=self.kwargs['id_pk'])
        return obj

    form_class = SutartisUpdateForm
    form_valid_message = 'Sutartis pataisyta!'
    template_name = 'sutartis_form.html'
    # k = get_object(queryset=None)

    # success_url = reverse_lazy('sutartis_view', kwargs={'kodas': ''})

    def form_valid(self, form):
        ''' Atlikus POST suvienodina imones pavadinimo uzrasyma. Pvz., "IMONESPAVADINIMAS, UAB"

        :param form:
        :return:
        '''
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


@login_required()
def sutartis_copy(request, id_pk):
    ''' Kopijuoja sutarti. Atidaro forma redagavimui is klases SutartisUpdate (sutartis_form.html).

    Kopijavimas padarytas tam, kad maziau duomenu reiketu suvedineti ranka.
    Nukopijavus tereikia pakeisti besiskiriancius duomenis.

    :param request:
    :param id_pk:
    :return:
    '''
    nauja = Sutartis.objects.get(pk=id_pk)
    nauja.pk = None
    nauja.save()
    return redirect('sutartis_update', id_pk=nauja.pk)
    # return render(request, 'sutartis.html')


'''
    def form_valid(self, form):
        form.instance.kodas = Planas.objects.get(kodas=self.kwargs['kodas'])
        return super(SutartisUpdate, self).form_valid(form)
'''


@login_required()
def sutartis_delete_confirm(request, id_pk):
    context = {
        'id_pk': Sutartis.objects.get(pk=id_pk).id,
        'kodas': Sutartis.objects.get(pk=id_pk),
        'debug': 'DEBUG'
    }
    # return render(request, 'kodas_view.html', context)
    return render(request, 'sutartis_delete_confirm.html', context)


class SutartisDelete(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.DeleteView):
    # form_class = PlanasDeleteForm
    # form_valid_message = 'Planas pataisytas!'
    template_name = 'sutartis_delete_confirm.html'
    model = Sutartis
    form_valid_message = 'Sutartis sėkmingai ištrinta.'

    # success_url = reverse_lazy('planas')

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


@login_required()
def laikotarpis(request):
    ''' Filtruojamo laikotarpio nustatymui ir VP kodui pasirinkti.

    Parodo langa pries sutarties pildyma (zurnalo_laikotarpis.html).
    Jame galima nusistatyti filtruojama laikotarpi ir butina pasirinkti
    VP koda, kuriuo bus pildoma sutartis.

    :param request:
    :return:
    '''
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


class SutartisAdd(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.CreateView):

    form_class = SutartisUpdateForm
    form_valid_message = 'Pridėta nauja sutartis.'
    template_name = 'sutartis_form.html'

    # k = get_object(queryset=None)

    # success_url = reverse_lazy('sutartis_view', kwargs={'kodas': ''})

    def form_valid(self, form):
        ''' Atlikus POST, suvienodina imones pavadinimo uzrasyma. Pvz., "IMONESPAVADINIMAS, UAB"

        :param form:
        :return:
        '''
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


