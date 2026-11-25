"""Formularios de la zona de administración de la galería."""
from django import forms

from config.formularios import EstiloBootstrapMixin

from .models import Categoria, Imagen


class FormularioCategoria(EstiloBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]


class FormularioImagen(EstiloBootstrapMixin, forms.ModelForm):
    """Solo admite JPG y PNG (lo valida el modelo)."""

    class Meta:
        model = Imagen
        fields = ["archivo", "categoria", "numero_likes", "numero_visitas", "numero_descargas"]
