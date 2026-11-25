"""Consulta de los mensajes de contacto en el panel /admin/."""
from django.contrib import admin

from .models import Contacto


@admin.register(Contacto)
class AdministradorContactos(admin.ModelAdmin):
    list_display = ("asunto", "nombre", "apellidos", "email")
    search_fields = ("asunto", "nombre", "apellidos", "email", "mensaje")
