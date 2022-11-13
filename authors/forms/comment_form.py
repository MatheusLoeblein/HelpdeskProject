from django import forms

from helpdesk.models import Comment
from utils.django_forms import add_attr


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('name'), 'css', 'span-2')
        add_attr(self.fields.get('comment'), 'css', 'span-2')

    class Meta:
        model = Comment
        fields = ['comment', 'name']

        widgets = {
            'name': forms.Select(
                choices=(
                    ('Resposta', 'Resposta'),
                    ('Complemento', 'Complemento'),
                ))}
