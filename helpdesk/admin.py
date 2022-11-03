from django.contrib import admin

from .models import Category, Comment, Tarefa

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


class TarefaAdmin(admin.ModelAdmin):
    list_display = ['ticketid', 'id', 'title', 'data_at', 'data_up_at']
    list_display_links = 'title',
    search_fields = ['id', 'title', 'data_at',
                     'Category', 'ticketid', 'author', 'prioridade', ]
    list_filter = 'Category', 'author',
    list_per_page = 15
    ordering = '-data_up_at',


class CommentAdmin(admin.ModelAdmin):
    ...


admin.site.register(Tarefa, TarefaAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment, CommentAdmin)
