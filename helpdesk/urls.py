from django.urls import path

from . import views

app_name = 'helpdesk'

urlpatterns = [
    path('', views.home, name="home"),
    path('tarefa/search/', views.search, name="search"),
    path('tarefa/category/<int:Category_id>/',
         views.category, name="tarefas-category"),
    path('tarefa/<int:id>/', views.tarefa, name="tarefa"),
    path('tarefa/addcomment/<int:id>', views.addcomment, name="addcomment"),
<<<<<<< HEAD
    path('status/', views.situacao, name="status"),
    path('prioridade/', views.prioridade, name="prioridade"),
=======
    path('status/', views.status, name="status"),
    path('finalizados/', views.finalizado, name="finalizado")
>>>>>>> 72527e843dae0d3875bfbe9aca44b61a8e051cf3
]
