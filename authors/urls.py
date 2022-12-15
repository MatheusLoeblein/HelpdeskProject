from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('register/create/', views.register_create, name="register_create"),
    path('login/', views.login_view, name="login"),
    path('login/create/', views.login_create, name="login_create"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/tarefa/new/', views.dashboard_tarefa_new,
         name="dashboard_tarefa_new"),
    path('dashboard/tarefa/<int:id>/edit/', views.dashboard_tarefa_edit,
         name="dashboard_tarefa_edit"),
    path('dashboard/tarefa/delete/', views.dashboard_tarefa_delete,
         name="dashboard_tarefa_delete"),
    path('dashboard/export/xlsx/', views.export_tarefas_xlsx,
         name="dashboard_export_xlsx"),
    path('dashboard/addprofileimg/',
         views.addprofileimg, name="addprofileimg"),
    path('maquinas/', views.maquinas, name="maquinas"),
    path('maquina/view/', views.addmaquina_view, name="maquina_view"),
    path('maquina/new/', views.addmaquina, name="maquina_new"),
    path('maquina/<int:id>/edit/', views.maquina_edit, name="maquina_edit"),
    path('maquina/delete/', views.maquina_delete, name="maquina_delete"),
]
