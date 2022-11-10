from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, get_list_or_404, render

from authors.forms import CommentForm
from utils.pagination import make_pagination_range

from .models import Comment, Tarefa


# Create your views here.
def home(request):
    tarefas = Tarefa.objects.all().order_by('-data_up_at')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(tarefas, 30)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(request, "helpdesk/pages/home.html", context={
        'tarefas': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, Category_id):
    tarefas = get_list_or_404(Tarefa.objects.filter(
        Category__id=Category_id,

    ).order_by('-data_at'))
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

            messages.success(request, 'Seu Comentario foi salvo com sucesso!')

            return (HttpResponseRedirect(url))

        messages.error(request, 'Comentario Invalido.')
    return (HttpResponseRedirect(url))
