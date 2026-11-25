"""Vistas de usuarios: registro. El login y el logout usan las vistas de Django."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import FormularioRegistro


def registro(request):
    """Crea la cuenta y deja al usuario con la sesión iniciada."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    formulario = FormularioRegistro(request.POST or None)
    if formulario.is_valid():
        usuario = formulario.save()
        login(request, usuario)
        messages.success(request, f"Bienvenido, {usuario.nombre}. Tu cuenta se ha creado correctamente.")
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "usuarios/registro.html", {"formulario": formulario})
