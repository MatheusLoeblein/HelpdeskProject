import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image

from helpdesk.models import Category

User = get_user_model()


class Usuariofc(models.Model):
    name = models.CharField(
        max_length=9, verbose_name='Usuario Fórmula Certa')

    def __str__(self):
        return self.name


class IP(models.Model):
    numero = models.GenericIPAddressField(verbose_name='IP')

    def __str__(self):
        return str(self.numero)


class impressora(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Impressora')
    ip = models.OneToOneField(
        IP, on_delete=models.CASCADE,  verbose_name='IP Address')
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')  # noqa
    mac = models.CharField(max_length=17, verbose_name='MAC')


class Maquinas(models.Model):
    ativo = models.BooleanField(
        default=False, verbose_name="Máquina Ativa")
    nome = models.CharField(max_length=30, verbose_name='Nome da Máquina')
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')  # noqa
    config = models.CharField(
        max_length=100, verbose_name='Configurações da máquina')
    anydesk = models.CharField(max_length=11, verbose_name='Anydesk')
    usuario2 = models.CharField(
        max_length=30, verbose_name='Usuario Temporario', null=True, blank=True)  # noqa
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuario')  # noqa
    ramal = models.CharField(max_length=4, null=True, verbose_name='Ramal')
    email = models.CharField(max_length=65, verbose_name='E-Mail')
    skype = models.CharField(max_length=65, verbose_name='Skype ID')
    windows = models.CharField(max_length=6, verbose_name='Versão do Windows')
    ip = models.OneToOneField(
        IP, on_delete=models.CASCADE,  verbose_name='IP Address')
    usuariofc = models.OneToOneField(
        Usuariofc, on_delete=models.CASCADE, verbose_name='Fórmula Certa')  # noqa
    celular = models.CharField(
        max_length=11, null=True, verbose_name='Numero de Celular')
    gmail = models.CharField(max_length=65, null=True,
                             verbose_name='Conta Google')
    e7 = models.BooleanField(
        default=False, verbose_name='E7 Antivirus')
    office = models.BooleanField(
        default=False, verbose_name='Pacote Office')
    data_at = models.DateTimeField(auto_now_add=True)
    data_up_at = models.DateTimeField(auto_now=True)
    mac = models.CharField(max_length=17, null=True,
                           blank=True, verbose_name='MAC')

    def __str__(self):
        return self.nome


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    cover_profile = models.ImageField(upload_to='helpdesk/profile/imgs/%Y/%m/%d/',  # noqa
                                      blank=True, null=True, verbose_name='Foto de perfil')  # noqa
    maquina = models.ForeignKey(
        Maquinas, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Máquina')  # noqa

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
                self.resize_image(self.cover_profile, 100)
            except FileNotFoundError:
                ...
        return saved
