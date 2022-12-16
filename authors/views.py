import os
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse

from authors.models import Maquinas, Profile
from helpdesk.models import Tarefa
from utils.helpdesk.export_xlsx import export_xlsx
from utils.pagination import make_pagination

from .forms import (AuthorTarefaForm, LoginForm, MaquinasForm, ProfileForm,
                    RegisterForm)

PER_PAGE = os.environ.get('PER_PAGE', 25)


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request, 'Usuario Criado, por favor efetue o log in.')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:dashboard')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, ' Você esta logado. ')
            login(request, authenticated_user)
        else:
            messages.error(request, ' Usuario ou senha invalidos. ')

    else:
        messages.error(request, ' Erro na validação do formulario ')

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.success(request, 'Você esta deslogado.!')
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    tarefas = Tarefa.objects.filter(
        author=request.user,
    )
    tarefas_a = Tarefa.objects.filter(
        author=request.user,
        status='Aberto'
    )
    tarefas_e = Tarefa.objects.filter(
        author=request.user,
        status='Execução'
    )
    tarefas_f = Tarefa.objects.filter(
        author=request.user,
        status='Finalizado'
    )

    tarefas_a = len(tarefas_a)
    tarefas_e = len(tarefas_e)
    tarefas_f = len(tarefas_f)

    page_obj, pagination_range = make_pagination(request, tarefas, PER_PAGE)

    return render(request, 'authors/pages/dashboard.html', {
        'tarefas': page_obj,
        'pagination_range': pagination_range,
        'tarefas_a': tarefas_a,
        'tarefas_e': tarefas_e,
        'tarefas_f': tarefas_f

    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_tarefa_edit(request, id):
    tarefa = Tarefa.objects.filter(
        author=request.user,
        pk=id,
        status="Aberto",
    ).first()

    if not tarefa:
        raise Http404()

    form = AuthorTarefaForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=tarefa
    )

    if form.is_valid():
        # Agora, o form é valido e eu posso tentar salvar
        tarefa = form.save(commit=False)

        # se o usuario da sessão for o mesmo que criou a tarefa..
        tarefa.author = request.user

        tarefa.save()

        messages.success(request, 'Sua tarefa foi salva com sucesso!')

        return redirect(reverse('authors:dashboard'))

    return render(request, 'authors/pages/dashboard_tarefa.html', {
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_tarefa_new(request):

    form = AuthorTarefaForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        # Agora, o form é valido e eu posso tentar salvar
        tarefa = form.save(commit=False)

        # se o usuario da sessão for o mesmo que criou a tarefa..
        tarefa.author = request.user
        tarefa.setor_author = request.user.profile.Category

        tarefa.save()

        messages.success(request, 'tarefa criada com sucesso.')

        #return redirect(reverse('authors:dashboard_tarefa_edit', args=(tarefa.id,)))  # noqa
        return redirect(reverse('helpdesk:home'))

    return render(request, 'authors/pages/dashboard_tarefa.html', {
        'form': form,
        'form_action': reverse('authors:dashboard_tarefa_new'),

    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_tarefa_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    tarefa = Tarefa.objects.filter(
        author=request.user,
        pk=id,
    ).first()

    if not tarefa:
        raise Http404()

    tarefa.delete()
    messages.success(request, 'Tarefa apagada com Sucesso.')
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def export_tarefas_xlsx(request):
    mdata = datetime.now().strftime('%Y-%m-%d')
    model = 'Tarefa'
    filename = 'produtos_exportados.xls'
    __filename = filename.split('.')
    filename_final = f'{__filename[0]}_{mdata}.{__filename[1]}'

    queryset = Tarefa.objects.all().values_list('title', 'description', 'prioridade',  # noqa
                                                'status', 'Category', 'author')

    columns = ['Titulo', 'Descrição', 'Prioridade', 'Status',
               'Setor', 'Autor']

    response = export_xlsx(model, filename_final, queryset, columns)
    return response


@login_required(login_url='authors:login', redirect_field_name='next')
def addprofileimg(request):

    usuario = Profile.objects.get(author=request.user)

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=usuario)

        if form.is_valid():

            foto = form.save(commit=False)
            foto.save()

            messages.success(request, 'Foto adicionada com Sucesso!')

            return (HttpResponseRedirect(url))

        messages.error(request, 'Erro ao adicionar Foto.')
    return (HttpResponseRedirect(url))


@login_required(login_url='authors:login', redirect_field_name='next')
def maquinas(request):

    maquinas = Maquinas.objects.all()

    return render(request, 'authors/pages/maquinas.html', {
        'maquinas': maquinas,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def addmaquina_view(request):

    form = MaquinasForm()

    return render(request, 'authors/pages/maquinas_new.html', {
        'form': form,
        'form_action': reverse('authors:maquina_new'),
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def addmaquina(request):

    if not request.POST:
        raise Http404()

    form = MaquinasForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():

        maquina = form.save(commit=False)

        maquina.save()

        messages.success(request, 'Máquina Cadastrada com sucesso.')

        return redirect(reverse('authors:maquinas'))

    return render(request, 'authors/pages/maquinas_new.html', {
        'form': form,
        'form_action': reverse('authors:maquina_new'),

    })


@login_required(login_url='authors:login', redirect_field_name='next')
def maquina_edit(request, id):

    if not request.user.is_superuser:
        messages.error(
            request, 'Você não tem permissão suficiente, acione a administração.')  # noqa

        return redirect(reverse('authors:maquinas'))

    maquina = Maquinas.objects.filter(
        pk=id
    ).first()

    if not maquina:
        raise Http404()

    form = MaquinasForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=maquina
    )

    if form.is_valid():

        maquina = form.save(commit=False)

        maquina.save()

        messages.success(request, 'Máquina Salva com sucesso.')

        return redirect(reverse('authors:maquinas'))

    return render(request, 'authors/pages/maquinas_new.html', {
        'form': form,

    })


@login_required(login_url='authors:login', redirect_field_name='next')
def maquina_delete(request):

    if not request.user.is_superuser:
        messages.error(
            request, 'Você não tem permissão suficiente, acione a administração.')  # noqa

        return redirect(reverse('authors:maquinas'))

    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    maquina = Maquinas.objects.get(
        pk=id
    )

    if not maquina:
        raise Http404()

    maquina.delete()

    messages.success(request, 'Máquina deletada com sucesso.')
    return redirect(reverse('authors:maquinas'))
