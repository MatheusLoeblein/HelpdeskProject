from collections import defaultdict

from django import forms
from django_summernote.widgets import SummernoteWidget

from helpdesk.models import Comment
from utils.django_forms import add_attr


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('status_modify'), 'class', 'span-2')
        add_attr(self.fields.get('comment'), 'class', 'span-2')

    comment = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Comment
        fields = ['comment', 'status_modify', 'cover']
