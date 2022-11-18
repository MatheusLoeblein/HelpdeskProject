from django.contrib import admin

from .models import Category, Comment, Tarefa

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


class TarefaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'data_at', 'data_up_at']
    list_display_links = 'title',
    search_fields = ['id', 'title', 'data_at',
                     'Category', 'author', 'prioridade', ]
    list_filter = 'Category', 'author',
    list_per_page = 15
    ordering = '-data_up_at',


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'comment', 'Tarefa', 'created_at']
    list_display_links = 'name',
    search_fields = ['id', 'name', 'Tarefa', 'created_at']
    list_filter = ['id', 'name', 'Tarefa', 'created_at']
    list_per_page = 15
    ordering = 'created_at',


admin.site.register(Tarefa, TarefaAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment, CommentAdmin)
