from django.contrib import admin

from .models import Category, Tarefa

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


class TarefaAdmin(admin.ModelAdmin):
    ...


admin.site.register(Tarefa, TarefaAdmin)

admin.site.register(Category, CategoryAdmin)
