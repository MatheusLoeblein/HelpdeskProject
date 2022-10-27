from django.urls import path

from helpdesk.views import home, tarefa

urlpatterns = [
    path('', home),
    path('tarefa/', tarefa),
]
