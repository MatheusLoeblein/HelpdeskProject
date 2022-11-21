from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from helpdesk.models import Tarefa
from utils.django_forms import add_attr


class AuthorTarefaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('title'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Tarefa
        fields = ['title',  'prioridade',
                  'Category', 'description', 'cover']
        widgets = {
            'prioridade': forms.Select(
                choices=(
                    ('Baixa', 'Baixa'),
                    ('Moderada', 'Moderada'),
                    ('Alta', 'Alta'),
                    ('Urgente', 'Urgente'),
                )
            ),
            'cover': forms.FileInput(attrs={
                'class': 'span-2'
            }
            )
        }
        Category = forms.CharField(label='Setor',
                                   error_messages={
                                       'required': 'Por favor selecione o seu "Setor"'}
                                   )

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        clean_data = self.cleaned_data
        title = clean_data.get('title')
        description = clean_data.get('description')
        category = clean_data.get('Category')

        if len(title) < 5:
            self._my_errors['title'].append(
                'O Titulo precisa de no minimo 5 Caracteres.')
        if len(title) > 35:
            self._my_errors['title'].append(
                'O Titulo não pode ter mais de 35 Caracteres.')

        if len(description) < 25:
            self._my_errors['description'].append(
                'A descrição da tarefa precisa de no minimo 25 Caracteres.')

        if title == description:
            self._my_errors['title'].append(
                'Você não pode repetir o mesmo que na descrição.')
            self._my_errors['description'].append(
                'Você não pode repetir o mesmo que no titulo.')

        if category is None:
            self._my_errors['Category'].append(
                'Por favor selecione o seu "Setor"')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
