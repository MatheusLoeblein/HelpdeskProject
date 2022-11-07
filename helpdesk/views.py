from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_list_or_404, redirect,
                              render)

from authors.forms import CommentForm

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

    comments = Comment.objects.filter(
        Tarefa__id=id).order_by('created_at')

    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': tarefa,
        'comments': comments,
    })


def search(request):
    #search_term = request.GET.get()
    return render(request, 'helpdesk/pages/search.html')


@login_required(login_url='authors:login', redirect_field_name='next')
def addcomment(request, id):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.name = form.cleaned_data['name']
            data.comment = form.cleaned_data['comment']
            data.Tarefa_id = id
            data.author = request.user
            data.save()
            return (HttpResponseRedirect(url))

    return (HttpResponseRedirect(url))


'''    POST = request.POST
    request.session['comment_form_data'] = POST
    form = CommentForm(POST)

    if form.is_valid():
        form = form.save()

        messages.success(request, 'Usuario Criado, por favor efetue o log in.')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')
'''
