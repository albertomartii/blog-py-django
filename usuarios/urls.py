"""Rutas de usuarios: login, logout y registro."""
from django.contrib.auth import views as vistas_autenticacion
from django.urls import path

from . import views

# Namespace: permite usar nombres como "usuarios:<ruta>" en plantillas y vistas
app_name = "usuarios"

urlpatterns = [
    path(
        "entrar/",
        vistas_autenticacion.LoginView.as_view(
            template_name="usuarios/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # Desde Django 5 el logout solo acepta POST (protección CSRF)
    path("salir/", vistas_autenticacion.LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),
]
