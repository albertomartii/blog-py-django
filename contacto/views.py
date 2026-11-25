"""Vistas de contacto: formulario y página de agradecimiento."""
from django.shortcuts import redirect, render

from .forms import FormularioContacto


def contacto(request):
    formulario = FormularioContacto(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect("contacto:gracias")
    return render(request, "contacto/contacto.html", {"formulario": formulario})


def gracias(request):
    return render(request, "contacto/gracias.html")
