from django.shortcuts import get_list_or_404, render
from utils.helpdesk.factory import make_recipe

from .models import Tarefa


# Create your views here.
def home(request):
    tarefas = Tarefa.objects.all().order_by('-data_at')
    return render(request, "helpdesk/pages/home.html", context={
        'tarefas': tarefas,
    })


def category(request, Category_id):
    tarefas = get_list_or_404(Tarefa.objects.filter(
        Category__id=Category_id).order_by('-data_at'))
    return render(request, "helpdesk/pages/category.html", context={
        'tarefas': tarefas,
        'title': f' Setor | {tarefas[0].Category.name}'
    })


def tarefa(request, id):
    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': [make_recipe(), ]
    })
