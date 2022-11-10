from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from helpdesk.models import Tarefa

from .forms import AuthorTarefaForm, LoginForm, RegisterForm


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
        author=request.user
    )
    return render(request, 'authors/pages/dashboard.html', {
        'tarefas': tarefas,

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
        instance=tarefa
    )

    if form.is_valid():
        # Agora, o form é valido e eu posso tentar salvar
        tarefa = form.save(commit=False)

        # se o usuario da sessão for o mesmo que criou a tarefa..
        tarefa.author = request.user

        tarefa.save()

        messages.success(request, 'Sua tarefa foi salva com sucesso!')

        return redirect(reverse('authors:dashboard_tarefa_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard_tarefa.html', {
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_tarefa_new(request):

    form = AuthorTarefaForm(
        data=request.POST or None
    )

    if form.is_valid():
        # Agora, o form é valido e eu posso tentar salvar
        tarefa = form.save(commit=False)

        # se o usuario da sessão for o mesmo que criou a tarefa..
        tarefa.author = request.user

        tarefa.save()

        messages.success(request, 'tarefa criada com sucesso.')

        return redirect(reverse('authors:dashboard_tarefa_edit', args=(tarefa.id,)))  # noqa

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
