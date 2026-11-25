"""Formulario de contacto."""
from django import forms

from config.formularios import EstiloBootstrapMixin

from .models import Contacto


class FormularioContacto(EstiloBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["nombre", "apellidos", "email", "asunto", "mensaje"]
