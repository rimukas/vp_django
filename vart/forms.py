from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field
from django import forms
from .models import Planas


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            ButtonHolder(
                Submit('register', 'Register', css_class='btn-primary')
            )
        )


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )


# Naujos prekes/paslaugos/darbo pridejimas
class PlanasAddForm(forms.ModelForm):

    class Meta:
        model = Planas
        fields = ['kodas', 'preke', 'islaidos', 'paslauga_darbas_preke']

    def __init__(self, *args, **kwargs):
#        self.user = kwargs.pop('user',None)
        super(PlanasAddForm, self).__init__(*args, **kwargs)
#        self.fields['organizatorius'].initial = 'redas'
        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'kodas',
            'preke',
            'islaidos',
            'paslauga_darbas_preke',
            ButtonHolder(
                Submit('add', 'Irasyti', css_class='btn-primary')
                ),
            )
