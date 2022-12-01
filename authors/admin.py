from django.contrib import admin

from authors.models import IP, Maquinas, Profile, Usuariofc


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(Usuariofc)
class UsuariofcAdmin(admin.ModelAdmin):
    ...


@admin.register(IP)
class IPAdmin(admin.ModelAdmin):
    ...


@admin.register(Maquinas)
class MaquinasAdmin(admin.ModelAdmin):
    ...
