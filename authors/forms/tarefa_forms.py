from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget

from helpdesk.models import Tarefa
from utils.django_forms import add_attr


class AuthorTarefaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('tipe'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    description = forms.CharField(label='Descrição', widget=SummernoteWidget())

    class Meta:
        model = Tarefa
        fields = ['tipe', 'local', 'prioridade',
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
        description = clean_data.get('description')
        category = clean_data.get('Category')
        tipe = clean_data.get('tipe')
        local = clean_data.get('local')

        if len(description) < 25:
            self._my_errors['description'].append(
                'A descrição da tarefa precisa de no minimo 25 Caracteres.')

        if tipe == description:
            self._my_errors['tipe'].append(
                'Você não pode repetir o mesmo que na descrição.')
            self._my_errors['description'].append(
                'Você não pode repetir o mesmo que no Tipo da tarefa.')

        if category is None:
            self._my_errors['Category'].append(
                'Por favor selecione o seu "Setor"')

        if local is None:
            self._my_errors['local'].append(
                'Por favor selecione o seu "Local"')

        if tipe is None:
            self._my_errors['tipe'].append(
                'Por favor selecione um "Tipo de tarefa"')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
