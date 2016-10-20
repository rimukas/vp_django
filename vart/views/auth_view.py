from django.views import generic
from braces import views
from vart.forms import RegistrationForm, LoginForm
from vart.models import Planas, Sutartis, Sf, User
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime


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

        data_nuo = date(date.today().year, 1, 1)
        data_iki = date(date.today())

        # kodas = get_object_or_404(Planas, kodas=kodas)

        planas = Planas.objects.filter(organizatorius=user_name)
        sutartys = Sutartis.objects.filter(kodas__kodas__in=planas)
        sutartys = sutartys.filter(
            data__range=[data_nuo, data_iki])
        fakturos = Sf.objects.filter(sutartisid_id__in=sutartys)

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
