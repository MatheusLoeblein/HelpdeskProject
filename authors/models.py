import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image

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

    @staticmethod
    def resize_image(image, new_width=60):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=100
        )

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)
        if self.cover_profile:
            try:
                self.resize_image(self.cover_profile, 60)
            except FileNotFoundError:
                ...
        return saved
