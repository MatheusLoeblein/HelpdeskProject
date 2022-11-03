from django import forms

from helpdesk.models import Tarefa


class AuthorTarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['title', 'description', 'prioridade', 'Category', 'status', ]
