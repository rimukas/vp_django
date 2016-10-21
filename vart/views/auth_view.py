from django.db.models import Sum, Count
from django.views import generic
from braces import views
from vart.forms import RegistrationForm, LoginForm
from vart.models import Planas, Sutartis
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from datetime import date


class HomePageView(generic.TemplateView):
    """ Pagrindinis (home) puslapis.

    TODO:
    Jame yra rodoma atskira informacija prisijungusiems ir
    neprisijungusiems vartotojams.

    """
    template_name = 'notlogged.html'

    def get_context_data(self, **kwargs):
        # turbut nereikalingas
        # context = super(HomePageView, self).get_context_data(**kwargs)
        user_name = self.request.user.username

        data_nuo = date(date.today().year, 1, 1)
        data_iki = date(date.today().year, date.today().month, date.today().day)

        # kodas = get_object_or_404(Planas, kodas=kodas)

        # gaunam visus vartotojui priklausancius VP plano kodus
        planas = Planas.objects.filter(organizatorius=user_name)

        # filtruojam ivestas sutartis pagal pradzios ir pabaigos data
        # sutartys = Sutartis.objects.filter(data__range=[data_nuo, data_iki])

        metai = date.today().year
        sutartys = Sutartis.objects.filter(data__year=metai)

        # dar prafiltruojam sutartis pagal prisijungusio vartotojo VP kodus (visus),
        # kad neimtu kitu vartotoju ivestu sutarciu
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
            'kodas__preke', 'kodas__kodas', 'kodas__islaidos').\
            annotate(
            sf_count=Count('sf__sf'),
            sf_sum=Sum('sf__suma'),
            proc=(Sum('sf__suma')/Sum('kodas__islaidos'))*100)

        context = {
            'fakturos': fakturos,
            'username': self.request.user.username,
            'data_nuo': data_nuo,
            'data_iki': data_iki,
            'laikotarpis': str(metai),
        }
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

    form_valid_message = 'Tu sėkmingai prisijungei '
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            self.form_valid_message += 'vartotojo ' + '"' + username + '"' + ' vardu.'
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
