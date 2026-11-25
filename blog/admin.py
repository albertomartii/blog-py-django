"""Gestión de publicaciones y comentarios en el panel /admin/."""
from django.contrib import admin

from .models import Comentario, Publicacion


class ComentarioEnLinea(admin.TabularInline):
    model = Comentario
    extra = 0


@admin.register(Publicacion)
class AdministradorPublicaciones(admin.ModelAdmin):
    list_display = ("titulo", "autor", "fecha_publicacion", "numero_likes")
    list_filter = ("fecha_publicacion",)
    search_fields = ("titulo", "contenido")
    readonly_fields = ("slug",)
    inlines = [ComentarioEnLinea]
