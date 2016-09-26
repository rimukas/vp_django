from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from .forms import LoginForm
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.shortcuts import render
from django.views import generic
from braces import views


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class SignUpView(generic.CreateView, views.AnonymousRequiredMixin, views.FormValidMessageMixin):
    form_valid_message = 'Tu sekmingai prisiregistravai!'
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'


class LoginView(generic.FormView, views.AnonymousRequiredMixin, views.FormValidMessageMixin):
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


class LogOutView(generic.RedirectView, views.LoginRequiredMixin, views.MessageMixin):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)
