from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields.get('username'), 'class', 'span-2')
        add_attr(self.fields.get('password'), 'class', 'span-2')
        add_attr(self.fields.get('first_name'), 'class', 'span-2')
        add_attr(self.fields.get('last_name'), 'class', 'span-2')
        add_attr(self.fields.get('username'), 'class', 'span-2')
        add_attr(self.fields.get('password2'), 'class', 'span-2')
        add_attr(self.fields.get('email'), 'class', 'span-2')

    username = forms.CharField(
        label='Usuario',
        help_text=(
            'O nome de usuário pode ter letras, números ou um desse caracteres @.+-_. '  # noqa
            'O comprimento deve estar entre 4 e 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo não deve estar vazio',
            'min_length': 'O nome de usuário deve ter pelo menos 4 caracteres',
            'max_length': 'O nome de usuário deve ter pelo menos 150 caracteres',  # noqa
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu primeiro nome'},
        label='Primeiro Nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Sobrenome'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail é requerido'},
        label='E-mail',
        help_text='O e-mail deve ser válido.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não deve estar vazia'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'span-2'
        },),
        label='Confirmação de senha',
        error_messages={
            'required': 'Por favor, repita sua senha'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            password_confirmation_error = ValidationError(
                'Senhas não são iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })


'''
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'E-mail do usuário já está em uso', code='invalid',
            )
        return email
'''
