"""Rutas de la galería: portada pública y administración."""
from django.urls import path

from . import views

# Namespace: permite usar nombres como "galeria:<ruta>" en plantillas y vistas
app_name = "galeria"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    # Prefijo "gestion/" para no chocar con el panel de Django en /admin/
    path("gestion/categorias/", views.administrar_categorias, name="categorias"),
    path("gestion/imagenes/", views.administrar_imagenes, name="imagenes"),
]
