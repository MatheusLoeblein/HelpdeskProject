from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Tarefa(models.Model):
    status_choices = (
        ("Aberto", "Aberto"),
        ("Em Andamento", "Em Andamento"),
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
        upload_to='tarefas/covers/%Y/%m/%d/', blank=False, null=False)
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    Tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
