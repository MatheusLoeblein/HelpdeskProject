from django.urls import path

from . import views

appname = 'helpdesk'

urlpatterns = [
    path('', views.home, name="home"),
    path('tarefa/search/', views.search, name="search"),
    path('tarefa/category/<int:Category_id>/',
         views.category, name="tarefas-category"),
    path('tarefa/<int:id>/', views.tarefa, name="tarefa"),
    path('tarefa/addcomment/<int:id>', views.addcomment, name="addcomment"),

]
