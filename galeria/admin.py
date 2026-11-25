"""Gestión de categorías e imágenes en el panel /admin/."""
from django.contrib import admin

from .models import Categoria, Imagen


@admin.register(Categoria)
class AdministradorCategorias(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(Imagen)
class AdministradorImagenes(admin.ModelAdmin):
    list_display = ("archivo", "categoria", "numero_visitas", "numero_likes", "numero_descargas")
    list_filter = ("categoria",)
