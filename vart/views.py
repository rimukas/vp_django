from .forms import PlanasAddForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from .forms import LoginForm
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic
from braces import views
from .models import Planas
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic.edit import CreateView


class HomePageView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['visas_vardas'] = ''
        return context


class SignUpView(
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.CreateView):
    form_valid_message = 'Tu sekmingai prisiregistravai!'
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'


class LoginView(
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.FormView):

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
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)


def PlanasView(request):
    # current_user = request.user.get_full_name()
    current_user = request.user.username
    context = {
        'current_user': current_user,
        'kodas': Planas.objects.filter(
            organizatorius_id=current_user).values()}
    return render(request, 'planas.html', context)


def KodasView(request, kodas_nr):
    context = {
        'kodas_nr': kodas_nr
    }
    return render(request, 'kodas_view.html', context)


'''
class PlanasAdd(generic.edit.CreateView):
    model = Planas
    fields = ['kodas', 'preke', 'islaidos']
    template_name = 'planas_add.html'
    form_valid_message = 'Kodas sėkmingai pridėtas'
    success_url = reverse_lazy('planas_add')

    # @method_decorator(login_required)
    def form_valid(self, form):
        form.instance.organizatorius = self.request.user
        return super(PlanasAdd, self).form_valid(form)
'''


class PlanasAdd(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.edit.CreateView):    
    form_class = PlanasAddForm
    form_valid_message = 'Nauja plano eilutė įvesta sėkmingai!'
    template_name = 'planas_create.html'
    success_url = reverse_lazy('planas_add')
   
 
    def form_valid(self, form):
        form.instance.organizatorius = self.request.user        
        return super(PlanasAdd, self).form_valid(form)
