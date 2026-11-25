"""Vistas de la galería: portada pública y zona de administración."""
from django.contrib import messages
from django.shortcuts import redirect, render

from config.permisos import solo_administradores

from .forms import FormularioCategoria, FormularioImagen
from .models import Categoria, Imagen


def inicio(request):
    """Portada: una pestaña por categoría con sus imágenes."""
    categorias = Categoria.objects.prefetch_related("imagenes")
    return render(request, "galeria/inicio.html", {"categorias": categorias})


@solo_administradores
def administrar_categorias(request):
    formulario = FormularioCategoria(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, "Categoría creada.")
        # Redirigir evita reenviar el formulario al recargar y muestra la lista actualizada
        return redirect("galeria:categorias")

    return render(request, "galeria/administrar_categorias.html", {
        "formulario": formulario,
        "categorias": Categoria.objects.all(),
    })


@solo_administradores
def administrar_imagenes(request):
    formulario = FormularioImagen(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, "Imagen subida.")
        return redirect("galeria:imagenes")

    return render(request, "galeria/administrar_imagenes.html", {
        "formulario": formulario,
        "imagenes": Imagen.objects.select_related("categoria"),
    })
