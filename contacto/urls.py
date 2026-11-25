"""Rutas del formulario de contacto."""
from django.urls import path

from . import views

# Namespace: permite usar nombres como "contacto:<ruta>" en plantillas y vistas
app_name = "contacto"

urlpatterns = [
    path("", views.contacto, name="contacto"),
    path("gracias/", views.gracias, name="gracias"),
]
