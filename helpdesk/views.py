from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_list_or_404, redirect,
                              render)
from django.urls import reverse

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

    comment = Comment.objects.filter().first()

    comment_form_data = request.session.get('comment_form_data', None)
    form = CommentForm(comment_form_data)

    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': tarefa,
        'form': form,
        'comment': comment
    })


def search(request):
    #search_term = request.GET.get()
    return render(request, 'helpdesk/pages/search.html')


@login_required(login_url='authors:login', redirect_field_name='next')
def addcomment(request):

    POST = request.POST
    request.session['comment_form_data'] = POST
    form = CommentForm(POST)

    if form.is_valid():
        form = form.save()

        messages.success(request, 'Usuario Criado, por favor efetue o log in.')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')
