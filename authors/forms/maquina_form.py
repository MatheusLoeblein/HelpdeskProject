from django import forms

from authors.models import Maquinas
from utils.django_forms import add_attr


class MaquinasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields.get('email'), 'class', 'span-2')
        add_attr(self.fields.get('gmail'), 'class', 'span-2')
        add_attr(self.fields.get('config'), 'class', 'span-2')

    class Meta:
        model = Maquinas
        fields = '__all__'
