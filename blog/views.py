"""Vistas del blog: listado con búsqueda, detalle con comentarios, alta y likes."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import FormularioComentario, FormularioPublicacion
from .models import Publicacion

PUBLICACIONES_RECIENTES = 5


def _publicaciones_recientes():
    return Publicacion.objects.con_total_comentarios()[:PUBLICACIONES_RECIENTES]


def listado(request):
    """Listado paginado; si llega ?busqueda= filtra por contenido."""
    busqueda = request.GET.get("busqueda", "").strip()

    publicaciones = Publicacion.objects.con_total_comentarios().select_related("autor")
    if busqueda:
        publicaciones = publicaciones.filter(contenido__icontains=busqueda)

    paginador = Paginator(publicaciones, settings.PUBLICACIONES_POR_PAGINA)
    # get_page tolera valores no numéricos y páginas fuera de rango (devuelve la última)
    pagina_actual = paginador.get_page(request.GET.get("pagina"))

    return render(request, "blog/listado.html", {
        "pagina_actual": pagina_actual,
        "numeros_de_pagina": paginador.get_elided_page_range(pagina_actual.number, on_each_side=2, on_ends=1),
        "total": paginador.count,
        "busqueda": busqueda,
        "recientes": _publicaciones_recientes(),
    })


def detalle(request, slug):
    """Muestra una publicación con sus comentarios y recibe los comentarios nuevos."""
    publicacion = get_object_or_404(Publicacion.objects.con_total_comentarios().select_related("autor"), slug=slug)

    formulario = FormularioComentario(request.POST or None)
    if formulario.is_valid():
        comentario = formulario.save(commit=False)
        comentario.publicacion = publicacion
        comentario.save()
        messages.success(request, "Gracias por tu comentario.")
        # Redirigir evita reenviar el formulario al recargar la página
        return redirect("blog:detalle", slug=publicacion.slug)

    return render(request, "blog/detalle.html", {
        "publicacion": publicacion,
        "comentarios": publicacion.comentarios.all(),
        "formulario": formulario,
        "recientes": _publicaciones_recientes(),
    })


@login_required
def nueva_publicacion(request):
    """Alta de publicaciones: solo usuarios con sesión, que quedan como autores."""
    formulario = FormularioPublicacion(request.POST or None)
    if formulario.is_valid():
        publicacion = formulario.save(commit=False)
        publicacion.autor = request.user
        publicacion.save()
        messages.success(request, "La publicación se ha creado correctamente.")
        return redirect("blog:detalle", slug=publicacion.slug)

    return render(request, "blog/nueva_publicacion.html", {"formulario": formulario})


@require_POST
def dar_like(request, slug):
    """Suma un like y devuelve el total en JSON. Solo POST: un GET no debe modificar datos."""
    publicacion = get_object_or_404(Publicacion, slug=slug)
    publicacion.registrar_like()
    return JsonResponse({"correcto": True, "likes": publicacion.numero_likes})
