"""Gestión de usuarios en el panel /admin/ con identificación por email."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import FormularioCreacionUsuarioAdmin, FormularioEdicionUsuarioAdmin
from .models import Usuario


@admin.register(Usuario)
class AdministradorUsuarios(UserAdmin):
    form = FormularioEdicionUsuarioAdmin
    add_form = FormularioCreacionUsuarioAdmin

    list_display = ("email", "nombre", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "nombre")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Datos personales", {"fields": ("nombre",)}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas importantes", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "nombre", "password1", "password2")}),
    )
