from django import forms

from helpdesk.models import Tarefa
from utils.django_forms import add_attr


class AuthorTarefaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('title'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')

    class Meta:
        model = Tarefa
        fields = ['title',  'prioridade',
                  'Category', 'description', ]
        widgets = {
            'prioridade': forms.Select(
                choices=(
                    ('Urgencia', 'Urgencia'),
                    ('Alta', 'Alta'),
                    ('Moderada', 'Moderada'),
                    ('Baixa', 'Baixa'),
                )
            )
        }
        Category = forms.CharField(
            error_messages={'required': 'Por favor selecione o seu "Setor"'},
            label='Setor'
        )
