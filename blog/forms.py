"""Formularios del blog: alta de publicaciones y comentarios."""
from django import forms

from config.formularios import EstiloBootstrapMixin

from .models import Comentario, Publicacion


class FormularioPublicacion(EstiloBootstrapMixin, forms.ModelForm):
    """El slug, el autor y los likes no se piden: los fija la vista o el modelo."""

    class Meta:
        model = Publicacion
        fields = ["titulo", "contenido", "imagen"]


class FormularioComentario(EstiloBootstrapMixin, forms.ModelForm):
    """La publicación y la fecha no se piden al visitante: las fija la vista."""

    class Meta:
        model = Comentario
        fields = ["nombre", "email", "texto"]
