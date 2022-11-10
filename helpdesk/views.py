import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import HttpResponseRedirect, get_list_or_404, render

from authors.forms import CommentForm
from utils.pagination import make_pagination

from .models import Comment, Tarefa

PER_PAGE = os.environ.get('PER_PAGE', 25)

# Create your views here.


def home(request):
    tarefas = Tarefa.objects.all().order_by('-data_up_at')

    page_obj, pagination_range = make_pagination(request, tarefas, PER_PAGE)

    return render(request, "helpdesk/pages/home.html", context={
        'tarefas': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, Category_id):
    tarefas = get_list_or_404(Tarefa.objects.filter(
        Category__id=Category_id,
    ).order_by('-data_up_at'))

    page_obj, pagination_range = make_pagination(request, tarefas, PER_PAGE)

    return render(request, "helpdesk/pages/category.html", context={
        'tarefas': page_obj,
        'pagination_range': pagination_range,
        'title': f' Setor | {tarefas[0].Category.name}'
    })


def tarefa(request, id):
    tarefa = Tarefa.objects.filter(
        pk=id).first()

    comments = Comment.objects.filter(
        Tarefa__id=id).order_by('created_at')

    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': tarefa,
        'comments': comments,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    tarefas = Tarefa.objects.filter(
        Q(Q(title__icontains=search_term) | Q(
            status__icontains=search_term) | Q(id__icontains=search_term)),
    ).order_by('-data_up_at')

    page_obj, pagination_range = make_pagination(request, tarefas, PER_PAGE)

    return render(request, 'helpdesk/pages/search.html', {
        'page_title': f'Pesquisa por "{search_term}"',
        'search_term': search_term,
        'tarefas': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })


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

            messages.success(request, 'Seu Comentario foi salvo com sucesso!')

            return (HttpResponseRedirect(url))

        messages.error(request, 'Comentario Invalido.')
    return (HttpResponseRedirect(url))
