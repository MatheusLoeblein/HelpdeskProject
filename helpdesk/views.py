import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import HttpResponseRedirect, get_list_or_404, render

from authors.forms import CommentForm
from authors.models import Profile
from utils.pagination import make_pagination

from .models import Comment, Tarefa

PER_PAGE = os.environ.get('PER_PAGE', 25)

# Create your views here.


@login_required(login_url='authors:login', redirect_field_name='next')
def home(request):

    if request.user.is_superuser:
        tarefas = Tarefa.objects.all().order_by('-data_up_at')
    else:
        usuario = Profile.objects.get(author=request.user)

        tarefas = Tarefa.objects.filter(
            Category=usuario.Category_id).order_by('-data_up_at')

    page_obj, pagination_range = make_pagination(request, tarefas, PER_PAGE)

    return render(request, "helpdesk/pages/home.html", context={
        'tarefas': page_obj,
        'pagination_range': pagination_range,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
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


@login_required(login_url='authors:login', redirect_field_name='next')
def tarefa(request, id):
    tarefa = Tarefa.objects.filter(
        pk=id).first()

    comments = Comment.objects.filter(
        Tarefa__id=id).order_by('created_at')

    return render(request, "helpdesk/pages/tarefa.html", context={
        'tarefa': tarefa,
        'comments': comments,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def search(request):
    search_term = request.GET.get('q', '').strip()
    usuario = Profile.objects.get(author=request.user)
    usuario = usuario.Category_id
    if not search_term:
        raise Http404()

    tarefas = Tarefa.objects.filter(Category=usuario).filter(
        Q(Q(title__icontains=search_term) | Q(
            status__icontains=search_term) | Q(id__icontains=search_term)),
    ).order_by('-data_up_at')

    page_obj, pagination_range = make_pagination(request, tarefas, PER_PAGE)

    return render(request, 'helpdesk/pages/search.html', {
        'page_title': f'Pesquisa por "{search_term}"',
        'search_term': search_term,
        'tarefas': page_obj,
        'pagination_range': pagination_range,

    })


@login_required(login_url='authors:login', redirect_field_name='next')
def addcomment(request, id):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        status = request.POST.get('status_modify', None)
        if form.is_valid():
            data = Comment()
            data.comment = form.cleaned_data['comment']
            if not status == None:
                data.status_modify = form.cleaned_data['status_modify']
            data.cover = form.cleaned_data['cover']
            data.Tarefa_id = id
            data.author = request.user
            data.save()

            messages.success(request, 'Seu Comentario foi salvo com sucesso!')

            return (HttpResponseRedirect(url))

        messages.error(request, 'Comentario Invalido.')
    return (HttpResponseRedirect(url))
