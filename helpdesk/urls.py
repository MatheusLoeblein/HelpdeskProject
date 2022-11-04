from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tarefa/search/', views.search, name="search"),
    path('tarefa/category/<int:Category_id>/',
         views.category, name="tarefas-category"),
    path('tarefa/<int:id>/', views.tarefa, name="tarefas"),
    path('tarefa/<int:id>/addcomment/', views.addcomment, name="addcomment"),

]
