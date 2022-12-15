from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Comment, Location, Tarefa, Tasktipe


class CategoryAdmin(admin.ModelAdmin):
    ...


class TasktipeAdmin(admin.ModelAdmin):
    ...


class LocationAdmin(admin.ModelAdmin):
    ...


class TarefaAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')
    list_display = ['id', 'tipe', 'setor_author',
                    'data_up_at', 'local', 'Category', 'author']
    list_display_links = 'tipe', 'setor_author',
    search_fields = ['id', 'setor_author', 'data_at',
                     'Category', 'author', 'prioridade', ]
    list_filter = 'Category', 'author', 'tipe', 'local'
    list_per_page = 15
    ordering = '-id',


'''
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'data_at', 'data_up_at']
    list_display_links = 'title',
    search_fields = ['id', 'title', 'data_at',
                     'Category', 'author', 'prioridade', ]
    list_filter = 'Category', 'author',
    list_per_page = 15
    ordering = '-data_up_at',
'''


class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('comment')
    list_display = ['id', 'name', 'comment', 'Tarefa', 'created_at']
    list_display_links = 'name',
    search_fields = ['id', 'name', 'Tarefa', 'created_at']
    list_filter = ['id', 'name', 'Tarefa', 'created_at']
    list_per_page = 15
    ordering = 'created_at',


admin.site.register(Tarefa, TarefaAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Tasktipe, TasktipeAdmin)

admin.site.register(Location, LocationAdmin)

admin.site.register(Comment, CommentAdmin)
