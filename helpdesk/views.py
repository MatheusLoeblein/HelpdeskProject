from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "helpdesk/pages/home.html")


def tarefa(request):
    return HttpResponse('TAREFA')
