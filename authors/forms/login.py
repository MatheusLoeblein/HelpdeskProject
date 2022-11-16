from django import forms

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields.get('username'), 'class', 'span-2')
        add_attr(self.fields.get('username'), 'label', 'span-2')
        add_attr(self.fields.get('password'), 'class', 'span-2')

    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Senha',
                               widget=forms.PasswordInput()
                               )
