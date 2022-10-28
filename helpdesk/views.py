from django.shortcuts import render
from utils.helpdesk.factory import make_recipe


# Create your views here.
def home(request):
    return render(request, "helpdesk/pages/home.html", context={
        'tarefas': [make_recipe() for _ in range(60)],
    })


def tarefa(request, id):
    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': [make_recipe(), ]
    })
