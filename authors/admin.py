from django.contrib import admin

from authors.models import IP, Maquinas, Profile, Usuariofc


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['author', 'id', 'Category']
    list_display_links = 'author',
    search_fields = ['id', 'Category', 'author', ]
    list_filter = 'Category',
    list_per_page = 15
    ordering = '-id',


@admin.register(Usuariofc)
class UsuariofcAdmin(admin.ModelAdmin):
    ordering = 'id',


@admin.register(IP)
class IPAdmin(admin.ModelAdmin):
    ordering = 'id',


@admin.register(Maquinas)
class MaquinasAdmin(admin.ModelAdmin):
    list_display = ['ativo', 'nome', 'usuario',
                    'Category', 'data_at', 'office', 'e7']
    list_display_links = 'nome',
    list_filter = ['Category', 'office', 'e7', 'windows', 'ativo']
    list_per_page = 15
    ordering = '-id',
