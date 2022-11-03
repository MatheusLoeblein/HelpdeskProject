from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, get_list_or_404, render

from .forms import CommentForm
from .models import Comment, Tarefa


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

    tarefa = Tarefa.objects.filter(
        pk=id).order_by('-id').first()

    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': tarefa,
    })


def search(request):
    #search_term = request.GET.get()
    return render(request, 'helpdesk/pages/search.html')


def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.name = form.cleaned_data['name']
            data.comment = form.cleaned_data['comment']
            data.Tarefa_id = id
            data.save()
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
