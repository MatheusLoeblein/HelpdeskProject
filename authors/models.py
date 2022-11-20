from django.contrib.auth import get_user_model
from django.db import models

from helpdesk.models import Category

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    cover_profile = models.ImageField(upload_to='helpdesk/profile/imgs/%Y/%m/%d/',
                                      blank=True, null=True, verbose_name='Foto de perfil')

    def __str__(self):
        return str(self.author)
