from django.contrib import admin

from .models import Category, Comment, Tarefa

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


class TarefaAdmin(admin.ModelAdmin):
    ...


class CommentAdmin(admin.ModelAdmin):
    ...


admin.site.register(Tarefa, TarefaAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment, CommentAdmin)
