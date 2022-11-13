from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Tarefa(models.Model):
    status_choices = (
        ("Aberto", "Aberto"),
        ("Execução", "Execução"),
        ("Fechado", "Fechado"),
    )
    title = models.CharField(max_length=65)
    description = models.TextField()
    prioridade = models.CharField(max_length=20)
    status = models.CharField(
        max_length=12, choices=status_choices, blank=False, null=False, default="Aberto")
    data_at = models.DateTimeField(auto_now_add=True)
    data_up_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(
        upload_to='helpdesk/covers/%Y/%m/%d/', blank=True, null=True)
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    Tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, )
    name = models.CharField(max_length=255, blank=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.Tarefa)


@receiver(post_save, sender=Comment)
def update_data(sender, instance, **kwargs):
    instance.Tarefa.data_up_at = instance.created_at
    instance.Tarefa.save()
