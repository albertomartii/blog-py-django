"""Rutas del blog: listado, alta, detalle y likes."""
from django.urls import path

from . import views

# Namespace: permite usar nombres como "blog:<ruta>" en plantillas y vistas
app_name = "blog"

urlpatterns = [
    path("blog/", views.listado, name="listado"),
    path("blog/nueva/", views.nueva_publicacion, name="nueva"),
    path("publicacion/<slug:slug>/", views.detalle, name="detalle"),
    path("publicacion/<slug:slug>/like/", views.dar_like, name="like"),
]
