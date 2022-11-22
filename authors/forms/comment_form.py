from django import forms
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget

from helpdesk.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['status_modify', 'comment',  'cover']
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        }
