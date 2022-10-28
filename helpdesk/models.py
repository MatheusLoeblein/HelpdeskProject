from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Tarefa(models.Model):
    title = models.CharField(max_length=65)
    description = models.TextField()
    ticketid = models.SlugField(max_length=5)
    prioridade = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    data_at = models.DateTimeField(auto_now_add=True)
    data_up_at = models.DateTimeField(auto_now=True)
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
