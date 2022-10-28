from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tarefa/category/<int:Category_id>/',
         views.category, name="tarefas-category"),
    path('tarefa/<int:id>/', views.tarefa, name="tarefas")

]
