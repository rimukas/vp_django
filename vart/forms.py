from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML, Button, Field
from django import forms
from .models import Planas, Sutartis, Sf


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

        super(PlanasAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'kodas',
            'preke',
            'islaidos',
            'paslauga_darbas_preke',
            ButtonHolder(
                Submit('add', 'Įrašyti', css_class='btn-success'),
                Button('cancel', 'Grįžti neįrašius', css_class='btn-primary', onclick="window.history.back()"),
                ),

            # HTML('<br><a class="btn btn-warning" href={% url "planas" %}>Grįžti neįrašius</a>'),
            )


#  prekes/paslaugos/darbo redagavimas
class PlanasUpdateForm(forms.ModelForm):
    class Meta:
        model = Planas
        fields = ['kodas', 'preke', 'islaidos', 'paslauga_darbas_preke']

    def __init__(self, *args, **kwargs):

        super(PlanasUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'kodas',
            'preke',
            'islaidos',
            'paslauga_darbas_preke',
            ButtonHolder(
                Submit('add', 'Įrašyti', css_class='btn-success'),
                Button('cancel', 'Grįžti neįrašius', css_class='btn-primary', onclick="window.history.back()"),
                ),

            # HTML('<br><a class="btn btn-warning" href={% url "planas" %}>Grįžti neįrašius</a>'),
            )

    def clean(self):
        f = self.fields['data']
        print(f)
        return


#  prekes/paslaugos/darbo istrynimas
class PlanasDeleteForm(forms.ModelForm):

    class Meta:
        model = Planas
        fields = ['kodas', 'preke', 'islaidos', 'paslauga_darbas_preke']

    def __init__(self, *args, **kwargs):

        super(PlanasDeleteForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'kodas',
            'preke',
            'islaidos',
            'paslauga_darbas_preke',
            ButtonHolder(
                Submit('add', 'Ištrinti', css_class='btn-danger'),
                Button('cancel', 'Grįžti neįrašius', css_class='btn-default', onclick="window.history.back()"),
                ),
            # HTML('<br><a class="btn btn-warning" href={% url "planas" %}>Grįžti neįrašius</a>'),
            )


#  sutarties redagavimas
class SutartisUpdateForm(forms.ModelForm):

    class Meta:
        model = Sutartis
        fields = ['data', 'suma', 'tiekejo_kodas', 'tiekejas', 'pastaba', 'zalias']

    def __init__(self, *args, **kwargs):

        super(SutartisUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'data',
            'suma',
            'tiekejo_kodas',
            'tiekejas',
            'pastaba',
            'zalias',
            ButtonHolder(
                Submit('add', 'Įrašyti', css_class='btn-success'),
                Button('cancel', 'Grįžti neįrašius', css_class='btn-primary', onclick="window.history.back()"),
                ),

            # HTML('<br><a class="btn btn-warning" href={% url "planas" %}>Grįžti neįrašius</a>'),
            )


class LaikotarpisForm(forms.Form):
    date_from = forms.DateField()  # max_length=10
    date_to = forms.DateField()
    kodas = forms.CharField(max_length=30)


class SfForm(forms.ModelForm):

    class Meta:
        model = Sf
        fields = ['sf', 'data', 'suma', 'pavadinimas', 'sutartisid']

    def __init__(self, *args, **kwargs):
        super(SfForm, self).__init__(*args, **kwargs)

        self.fields['pavadinimas'].initial = SfForm.initial['pavadinimas']
        self.fields['suma'].initial = SfForm.initial['suma']
        self.fields['data'].initial = SfForm.initial['data']
        self.fields['sutartisid'].initial = SfForm.initial['sutartisid']
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'sf',
            'data',
            'suma',
            'pavadinimas',
            'sutartisid',
            ButtonHolder(
                Submit('add', 'Įrašyti', css_class='btn-success'),
                Button('cancel', 'Grįžti neįrašius', css_class='btn-primary', onclick="window.history.back()")
            )
        )
