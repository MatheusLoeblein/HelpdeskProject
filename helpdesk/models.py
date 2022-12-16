from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Tasktipe(models.Model):
    tipe = models.CharField(max_length=35, verbose_name='Tipo de Tarefa')

    def __str__(self):
        return self.tipe


class Location(models.Model):
    name = models.CharField(max_length=10, verbose_name='Local')

    def __str__(self):
        return self.name


class Tarefa(models.Model):
    status_choices = (
        ("Aberto", "Aberto"),
        ("Execução", "Execução"),
        ("Finalizado", "Finalizado"),
    )
    tipe = models.ForeignKey(
        Tasktipe, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de Tarefa')  # noqa
    setor_author = models.CharField(
        max_length=65, verbose_name='Setor do Autor', null=True, blank=True)
    description = models.TextField(verbose_name='Descrição')
    prioridade = models.CharField(max_length=20, verbose_name='Prioridade')
    status = models.CharField(
        max_length=12, choices=status_choices, blank=True, null=True, default="Aberto")  # noqa
    data_at = models.DateTimeField(auto_now_add=True)
    data_up_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(
        upload_to='helpdesk/covers/%Y/%m/%d/', blank=True, null=True, verbose_name='Anexo')  # noqa
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor Responsável')  # noqa
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    local = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Local')  # noqa
    global_msg = models.BooleanField(
        default=False, verbose_name='Mensagem Global')

    def __str__(self):
        return str(self.tipe)


class Comment(models.Model):
    status_choices = (
        ("Aberto", "Aberto"),
        ("Execução", "Execução"),
        ("Finalizado", "Finalizado"),

    )
    Tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, verbose_name='Tarefa')
    name = models.CharField(max_length=255, blank=False, default="Complemento")
    comment = models.TextField(verbose_name='Comentario')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    cover = models.ImageField(
        upload_to='helpdesk/covers/%Y/%m/%d/', blank=True, null=True, verbose_name='Anexo')  # noqa
    status_modify = models.CharField(
        max_length=12, choices=status_choices, blank=True, null=True, default="Aberto", verbose_name='Status')  # noqa


class Notification(models.Model):
    type_choices = (
        ("Comment", "Comment"),
        ("New Task", "New Task"),
        ("Status", "Status"),
    )
    type = models.CharField(
        max_length=8, choices=type_choices, blank=True, null=True)
    Tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, verbose_name='Tarefa')
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    created_at = models.DateTimeField(auto_now_add=True)
    visualization = models.BooleanField(default=False)


@receiver(post_save, sender=Comment)
def update_tarefa(sender, instance, **kwargs):
    instance.Tarefa.data_up_at = instance.created_at
    instance.Tarefa.status = instance.status_modify
    instance.Tarefa.save()
    if instance.Tarefa.status == "Finalizado":
        instance.Tarefa.prioridade = "Baixa"
        instance.Tarefa.save()
