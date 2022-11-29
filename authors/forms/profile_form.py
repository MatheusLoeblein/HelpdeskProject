from django import forms

from authors.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'cover_profile'
        ]
