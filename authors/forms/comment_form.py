from django import forms

from helpdesk.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['status_modify', 'comment',  'cover']
